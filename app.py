from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'spor_sitesi_gizli_anahtar_2024'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///spor_sitesi.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Veritabanı modelleri
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_admin = db.Column(db.Boolean, default=False)

class News(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String(500))
    category = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Match(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    home_team = db.Column(db.String(100), nullable=False)
    away_team = db.Column(db.String(100), nullable=False)
    home_score = db.Column(db.Integer, default=0)
    away_score = db.Column(db.Integer, default=0)
    match_date = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), default='scheduled')  # scheduled, live, finished
    sport_type = db.Column(db.String(50), nullable=False)

# Ana sayfa
@app.route('/')
def index():
    latest_news = News.query.order_by(News.created_at.desc()).limit(6).all()
    upcoming_matches = Match.query.filter_by(status='scheduled').order_by(Match.match_date).limit(4).all()
    live_matches = Match.query.filter_by(status='live').all()
    
    return render_template('index.html', 
                         latest_news=latest_news,
                         upcoming_matches=upcoming_matches,
                         live_matches=live_matches)

# Haberler sayfası
@app.route('/haberler')
def news():
    category = request.args.get('category', 'all')
    page = request.args.get('page', 1, type=int)
    
    if category != 'all':
        news_list = News.query.filter_by(category=category).order_by(News.created_at.desc()).paginate(
            page=page, per_page=9, error_out=False)
    else:
        news_list = News.query.order_by(News.created_at.desc()).paginate(
            page=page, per_page=9, error_out=False)
    
    return render_template('news.html', news_list=news_list, category=category)

# Haber detayı
@app.route('/haber/<int:news_id>')
def news_detail(news_id):
    news_item = News.query.get_or_404(news_id)
    related_news = News.query.filter_by(category=news_item.category).filter(
        News.id != news_id).limit(3).all()
    return render_template('news_detail.html', news=news_item, related_news=related_news)

# Maçlar sayfası
@app.route('/maclar')
def matches():
    sport_type = request.args.get('sport', 'all')
    status = request.args.get('status', 'all')
    
    query = Match.query
    
    if sport_type != 'all':
        query = query.filter_by(sport_type=sport_type)
    if status != 'all':
        query = query.filter_by(status=status)
    
    matches = query.order_by(Match.match_date.desc()).all()
    return render_template('matches.html', matches=matches, sport_type=sport_type, status=status)

# Giriş sayfası
@app.route('/giris', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, password):
            session['user_id'] = user.id
            session['username'] = user.username
            session['is_admin'] = user.is_admin
            flash('Başarıyla giriş yaptınız!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Kullanıcı adı veya şifre hatalı!', 'error')
    
    return render_template('login.html')

# Kayıt sayfası
@app.route('/kayit', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        if User.query.filter_by(username=username).first():
            flash('Bu kullanıcı adı zaten kullanılıyor!', 'error')
            return render_template('register.html')
        
        if User.query.filter_by(email=email).first():
            flash('Bu email adresi zaten kullanılıyor!', 'error')
            return render_template('register.html')
        
        user = User(
            username=username,
            email=email,
            password_hash=generate_password_hash(password)
        )
        db.session.add(user)
        db.session.commit()
        
        flash('Kayıt başarılı! Şimdi giriş yapabilirsiniz.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

# Çıkış
@app.route('/cikis')
def logout():
    session.clear()
    flash('Başarıyla çıkış yaptınız!', 'success')
    return redirect(url_for('index'))

# Admin paneli
@app.route('/admin')
def admin():
    if not session.get('is_admin'):
        flash('Bu sayfaya erişim yetkiniz yok!', 'error')
        return redirect(url_for('index'))
    
    news_count = News.query.count()
    user_count = User.query.count()
    match_count = Match.query.count()
    
    return render_template('admin.html', 
                         news_count=news_count,
                         user_count=user_count,
                         match_count=match_count)

# Admin - Haber ekleme
@app.route('/admin/haber-ekle', methods=['GET', 'POST'])
def admin_add_news():
    if not session.get('is_admin'):
        flash('Bu sayfaya erişim yetkiniz yok!', 'error')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        news = News(
            title=request.form['title'],
            content=request.form['content'],
            image_url=request.form['image_url'],
            category=request.form['category'],
            author_id=session['user_id']
        )
        db.session.add(news)
        db.session.commit()
        flash('Haber başarıyla eklendi!', 'success')
        return redirect(url_for('admin'))
    
    return render_template('admin_add_news.html')

# Admin - Maç ekleme
@app.route('/admin/mac-ekle', methods=['GET', 'POST'])
def admin_add_match():
    if not session.get('is_admin'):
        flash('Bu sayfaya erişim yetkiniz yok!', 'error')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        match = Match(
            home_team=request.form['home_team'],
            away_team=request.form['away_team'],
            match_date=datetime.strptime(request.form['match_date'], '%Y-%m-%dT%H:%M'),
            sport_type=request.form['sport_type']
        )
        db.session.add(match)
        db.session.commit()
        flash('Maç başarıyla eklendi!', 'success')
        return redirect(url_for('admin'))
    
    return render_template('admin_add_match.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        
        # Admin kullanıcısı oluştur (eğer yoksa)
        admin_user = User.query.filter_by(username='admin').first()
        if not admin_user:
            admin_user = User(
                username='admin',
                email='admin@sporsitesi.com',
                password_hash=generate_password_hash('admin123'),
                is_admin=True
            )
            db.session.add(admin_user)
            db.session.commit()
    
    app.run(debug=True, host='0.0.0.0', port=5000)