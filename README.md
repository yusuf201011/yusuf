import wx
import datetime
import threading
import time
import cv2

class RandevuUygulamasi(wx.Frame):
    def __init__(self, parent, title):
        super().__init__(parent, title=title, size=(700, 700))
        
        self.randevular = []  # Randevu listesi
        
        # Ana panel
        panel = wx.Panel(self)
        panel.SetBackgroundColour("#F0F8FF")
        
        # Başlık
        self.label = wx.StaticText(panel, label="Randevu Uygulamasına Hoş Geldiniz!", pos=(200, 20))
        font = wx.Font(14, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        self.label.SetFont(font)
        self.label.SetForegroundColour("#2F4F4F")
        
        # Butonlar
        ekle_btn = wx.Button(panel, label="Randevu Ekle", pos=(50, 100), size=(150, 50))
        ekle_btn.SetBackgroundColour("#ADD8E6")
        ekle_btn.SetForegroundColour("#000000")
        
        sil_btn = wx.Button(panel, label="Randevu Sil", pos=(250, 100), size=(150, 50))
        sil_btn.SetBackgroundColour("#FFB6C1")
        sil_btn.SetForegroundColour("#000000")
        
        listele_btn = wx.Button(panel, label="Randevuları Listele", pos=(450, 100), size=(150, 50))
        listele_btn.SetBackgroundColour("#90EE90")
        listele_btn.SetForegroundColour("#000000")
        
        cikis_btn = wx.Button(panel, label="Çıkış", pos=(300, 200), size=(100, 40))
        cikis_btn.SetBackgroundColour("#FFA07A")
        cikis_btn.SetForegroundColour("#000000")
        
        # Kamera alanı
        self.camera_panel = wx.Panel(panel, pos=(50, 300), size=(600, 300))
        self.camera_panel.SetBackgroundColour("#000000")
        
        # Event bağlama
        ekle_btn.Bind(wx.EVT_BUTTON, self.randevu_ekle)
        sil_btn.Bind(wx.EVT_BUTTON, self.randevu_sil)
        listele_btn.Bind(wx.EVT_BUTTON, self.randevulari_listele)
        cikis_btn.Bind(wx.EVT_BUTTON, self.cikis)
        
        # Kamera başlat
        self.init_camera()
        
        # Randevu kontrolü için bir thread başlat
        self.randevu_kontrol_thread = threading.Thread(target=self.randevu_kontrol)
        self.randevu_kontrol_thread.daemon = True
        self.randevu_kontrol_thread.start()
        
        self.Show()
    
    def init_camera(self):
        self.capture = cv2.VideoCapture(0)
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.update_camera, self.timer)
        self.timer.Start(100)  # 100ms aralıklarla kamera görüntüsünü güncelle
    
    def update_camera(self, event):
        ret, frame = self.capture.read()
        if ret:
            height, width = frame.shape[:2]
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image = wx.Bitmap.FromBuffer(width, height, frame)
            dc = wx.ClientDC(self.camera_panel)
            dc.DrawBitmap(image, 0, 0, False)
    
    def randevu_ekle(self, event):
        dialog = wx.TextEntryDialog(self, "Randevu bilgilerini girin (İsim, İşlem, Telefon, Tarih ve Saat):", "Randevu Ekle")
        if dialog.ShowModal() == wx.ID_OK:
            randevu_bilgisi = dialog.GetValue()
            self.randevular.append(randevu_bilgisi)
            wx.MessageBox("Randevu başarıyla eklendi!", "Bilgi", wx.OK | wx.ICON_INFORMATION)
        dialog.Destroy()
    
    def randevu_sil(self, event):
        dialog = wx.TextEntryDialog(self, "Silmek istediğiniz randevunun adını girin:", "Randevu Sil")
        if dialog.ShowModal() == wx.ID_OK:
            isim = dialog.GetValue()
            self.randevular = [r for r in self.randevular if not r.startswith(isim)]
            wx.MessageBox("Randevu başarıyla silindi!", "Bilgi", wx.OK | wx.ICON_INFORMATION)
        dialog.Destroy()
    
    def randevulari_listele(self, event):
        if not self.randevular:
            wx.MessageBox("Hiç randevu bulunmamaktadır.", "Bilgi", wx.OK | wx.ICON_INFORMATION)
        else:
            randevu_listesi = "\n".join(self.randevular)
            wx.MessageBox(f"Randevular:\n{randevu_listesi}", "Randevu Listesi", wx.OK | wx.ICON_INFORMATION)
    
    def randevu_kontrol(self):
        while True:
            now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
            for randevu in self.randevular:
                if now in randevu:
                    wx.CallAfter(wx.MessageBox, f"Randevu zamanı geldi: {randevu}", "Hatırlatma", wx.OK | wx.ICON_INFORMATION)
                    self.randevular.remove(randevu)
            time.sleep(60)
    
    def cikis(self, event):
        self.Close()
    
    def __del__(self):
        if hasattr(self, 'capture') and self.capture.isOpened():
            self.capture.release()
        if hasattr(self, 'timer'):
            self.timer.Stop()

if __name__ == "__main__":
    app = wx.App(False)
    frame = RandevuUygulamasi(None, "Randevu Uygulaması")
    app.MainLoop()
