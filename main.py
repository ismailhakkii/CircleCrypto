import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import math
import random
from typing import Dict, Tuple
import os

class EncryptionTheme:
    def __init__(self, name: str, colors: Dict[str, str]):
        self.name = name
        self.colors = colors

class CircularEncryption:
    def __init__(self):
        # Temaları tanımla
        self.themes = {
            'Klasik': EncryptionTheme('Klasik', {
                'background': '#FFFFFF',
                'circle': '#000000',
                'text': '#000000',
                'highlight': '#FF0000',
                'grid': '#CCCCCC'
            }),
            'Koyu': EncryptionTheme('Koyu', {
                'background': '#2C2C2C',
                'circle': '#FFFFFF',
                'text': '#FFFFFF',
                'highlight': '#00FF00',
                'grid': '#666666'
            }),
            'Mavi': EncryptionTheme('Mavi', {
                'background': '#E6F3FF',
                'circle': '#0066CC',
                'text': '#003366',
                'highlight': '#FF3366',
                'grid': '#99CCFF'
            })
        }
        self.current_theme = self.themes['Klasik']

        # Karakter setleri
        self.characters = {
            'küçük_harfler': 'abcçdefgğhıijklmnoöprsştuüvyz',
            'büyük_harfler': 'ABCÇDEFGĞHIİJKLMNOÖPRSŞTUÜVYZ',
            'rakamlar': '0123456789',
            'noktalama': '.,;\'`!?()_-"',
            'özel': '><|%/*-+\\}][{&¨~',
            'boşluk': ' \n\t'
        }
        self.generate_balanced_mapping()

    def generate_balanced_mapping(self):
        all_chars = ''.join(self.characters.values())
        chars_list = list(all_chars)
        random.shuffle(chars_list)

        chars_per_region = len(chars_list) // 4
        remaining = len(chars_list) % 4

        self.char_positions = {}
        current_char = 0

        for region in range(4):
            region_chars = chars_per_region + (1 if region < remaining else 0)
            start_angle = region * 90
            angle_step = 90 / (region_chars + 1)

            for i in range(region_chars):
                if current_char < len(chars_list):
                    char = chars_list[current_char]
                    angle = start_angle + ((i + 1) * angle_step)
                    self.char_positions[char] = round(angle, 1)
                    current_char += 1

class CircleCanvas(tk.Canvas):
    def __init__(self, parent, encryptor, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.encryptor = encryptor
        self.center = (300, 300)
        self.radius = 250
        self.bind('<Button-1>', self.on_click)
        self.selected_chars = []
        self.animation_active = False
        self.animation_char_index = 0
        self.animation_text = ""
        self.animation_speed = 500
        self.draw_circle()

    def draw_circle(self):
        theme = self.encryptor.current_theme.colors
        self.configure(bg=theme['background'])
        self.delete("all")
        self.create_circle()
        self.draw_region_lines()
        self.draw_degree_lines()
        self.place_characters()

    def create_circle(self):
        theme = self.encryptor.current_theme.colors
        x0 = self.center[0] - self.radius
        y0 = self.center[1] - self.radius
        x1 = self.center[0] + self.radius
        y1 = self.center[1] + self.radius
        self.create_oval(x0, y0, x1, y1, outline=theme['circle'], width=2)

    def draw_region_lines(self):
        theme = self.encryptor.current_theme.colors
        for angle in [0, 90, 180, 270]:
            rad = math.radians(angle)
            end_x = self.center[0] + self.radius * math.cos(rad)
            end_y = self.center[1] - self.radius * math.sin(rad)
            self.create_line(self.center[0], self.center[1], end_x, end_y,
                           fill=theme['grid'], width=2, dash=(5, 5))

        label_radius = self.radius * 0.5
        for i, angle in enumerate([45, 135, 225, 315]):
            rad = math.radians(angle)
            x = self.center[0] + label_radius * math.cos(rad)
            y = self.center[1] - label_radius * math.sin(rad)
            self.create_text(x, y, text=f"Bölge {i+1}",
                           fill=theme['text'], font=('Arial', 12, 'bold'))

    def place_characters(self):
                theme = self.encryptor.current_theme.colors
                for char, angle in self.encryptor.char_positions.items():
                    rad = math.radians(angle)

                    # Karakterin konumu
                    char_radius = self.radius * 0.85
                    x = self.center[0] + char_radius * math.cos(rad)
                    y = self.center[1] - char_radius * math.sin(rad)

                    # Karakteri yerleştir
                    text_color = theme['highlight'] if char in self.selected_chars else theme['text']
                    self.create_text(x, y, text=char, fill=text_color,
                                     font=('Arial', 12))

                    # Açı değeri
                    angle_radius = self.radius * 0.95
                    angle_x = self.center[0] + angle_radius * math.cos(rad)
                    angle_y = self.center[1] - angle_radius * math.sin(rad)
                    self.create_text(angle_x, angle_y, text=f"{angle}°",
                                     fill=theme['text'], font=('Arial', 8))

    def draw_degree_lines(self):
                theme = self.encryptor.current_theme.colors
                for angle in range(0, 360, 30):
                    rad = math.radians(angle)

                    # Çizgi
                    start_x = self.center[0] + (self.radius - 20) * math.cos(rad)
                    start_y = self.center[1] - (self.radius - 20) * math.sin(rad)
                    end_x = self.center[0] + self.radius * math.cos(rad)
                    end_y = self.center[1] - self.radius * math.sin(rad)

                    self.create_line(start_x, start_y, end_x, end_y,
                                     fill=theme['grid'])

                    # Derece yazısı
                    text_radius = self.radius + 20
                    text_x = self.center[0] + text_radius * math.cos(rad)
                    text_y = self.center[1] - text_radius * math.sin(rad)
                    self.create_text(text_x, text_y, text=f"{angle}°",
                                     fill=theme['text'], font=('Arial', 8))

    def animate_encryption(self, text):
                self.animation_text = text
                self.animation_char_index = 0
                self.animation_active = True
                self.animate_next_char()

    def animate_next_char(self):
                if not self.animation_active:
                    return

                if self.animation_char_index < len(self.animation_text):
                    char = self.animation_text[self.animation_char_index]
                    if char in self.encryptor.char_positions:
                        angle = self.encryptor.char_positions[char]
                        self.highlight_character(char, angle)
                    self.animation_char_index += 1
                    self.after(self.animation_speed, self.animate_next_char)
                else:
                    self.animation_active = False
                    self.draw_circle()

    def highlight_character(self, char, angle):
                self.draw_circle()
                theme = self.encryptor.current_theme.colors
                rad = math.radians(angle)

                # Karakteri vurgula
                char_radius = self.radius * 0.85
                x = self.center[0] + char_radius * math.cos(rad)
                y = self.center[1] - char_radius * math.sin(rad)

                self.create_text(x, y, text=char,
                                 fill=theme['highlight'],
                                 font=('Arial', 16, 'bold'))

                # Merkez-karakter arası çizgi
                self.create_line(self.center[0], self.center[1], x, y,
                                 fill=theme['highlight'], width=2)

    def on_click(self, event):
                if self.animation_active:
                    return

                x = event.x - self.center[0]
                y = self.center[1] - event.y
                click_angle = math.degrees(math.atan2(y, x))
                if click_angle < 0:
                    click_angle += 360

                # En yakın karakteri bul
                closest_char = None
                min_diff = 360

                for char, angle in self.encryptor.char_positions.items():
                    diff = abs(click_angle - angle)
                    if diff < min_diff and diff < 10:  # 10 derece tolerans
                        min_diff = diff
                        closest_char = char

                if closest_char:
                    if closest_char not in self.selected_chars:
                        self.selected_chars.append(closest_char)
                        self.highlight_character(closest_char,
                                                 self.encryptor.char_positions[closest_char])

class EncryptionApp(tk.Tk):
    def __init__(self):
                super().__init__()

                self.title("Gelişmiş Çemberli Şifreleme")
                self.encryptor = CircularEncryption()

                # Ana frame
                main_frame = ttk.Frame(self, padding="10")
                main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

                # Tema seçimi
                theme_frame = ttk.Frame(main_frame)
                theme_frame.grid(row=0, column=0, sticky=tk.W)

                ttk.Label(theme_frame, text="Tema:").pack(side=tk.LEFT)
                self.theme_var = tk.StringVar(value='Klasik')
                theme_combo = ttk.Combobox(theme_frame,
                                           textvariable=self.theme_var,
                                           values=list(self.encryptor.themes.keys()))
                theme_combo.pack(side=tk.LEFT, padx=5)
                theme_combo.bind('<<ComboboxSelected>>', self.change_theme)

                # Çember canvas
                self.circle_canvas = CircleCanvas(main_frame, self.encryptor,
                                                  width=600, height=600)
                self.circle_canvas.grid(row=1, column=0)

                # Kontrol butonları
                control_frame = ttk.Frame(main_frame)
                control_frame.grid(row=2, column=0, pady=10)

                ttk.Button(control_frame, text="Yeni Harita Oluştur",
                           command=self.new_mapping).pack(side=tk.LEFT, padx=5)
                ttk.Button(control_frame, text="Haritayı Kaydet",
                           command=self.save_mapping).pack(side=tk.LEFT, padx=5)
                ttk.Button(control_frame, text="Harita Yükle",
                           command=self.load_mapping).pack(side=tk.LEFT, padx=5)

                # Giriş/çıkış frame
                io_frame = ttk.Frame(main_frame)
                io_frame.grid(row=3, column=0, pady=10)

                # Giriş alanı
                ttk.Label(io_frame, text="Metin:").grid(row=0, column=0, sticky=tk.W)
                self.input_text = ttk.Entry(io_frame, width=50)
                self.input_text.grid(row=0, column=1, padx=5)

                # İşlem butonları
                ttk.Button(io_frame, text="Şifrele",
                           command=self.encrypt_text).grid(row=0, column=2, padx=5)
                ttk.Button(io_frame, text="Şifre Çöz",
                           command=self.decrypt_text).grid(row=0, column=3, padx=5)

                # Sonuç alanı
                ttk.Label(io_frame, text="Sonuç:").grid(row=1, column=0, sticky=tk.W)
                self.output_text = ttk.Entry(io_frame, width=50)
                self.output_text.grid(row=1, column=1, padx=5, pady=10)

                # Fare ile seçim sonucu
                ttk.Label(io_frame, text="Seçilen:").grid(row=2, column=0, sticky=tk.W)
                self.selected_text = ttk.Entry(io_frame, width=50)
                self.selected_text.grid(row=2, column=1, padx=5)
                ttk.Button(io_frame, text="Temizle",
                           command=self.clear_selection).grid(row=2, column=2, padx=5)

    def change_theme(self, event=None):
                theme_name = self.theme_var.get()
                self.encryptor.current_theme = self.encryptor.themes[theme_name]
                self.circle_canvas.draw_circle()

    def new_mapping(self):
                if messagebox.askyesno("Onay",
                                       "Yeni bir karakter haritası oluşturmak istiyor musunuz?"):
                    self.encryptor.generate_new_mapping()
                    self.circle_canvas.draw_circle()
                    messagebox.showinfo("Bilgi", "Yeni karakter haritası oluşturuldu.")

    def save_mapping(self):
                file_path = filedialog.asksaveasfilename(
                    defaultextension=".json",
                    filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
                    initialfile="karakter_haritasi.json"
                )
                if file_path:
                    try:
                        data = {
                            'mapping': self.encryptor.char_positions,
                            'theme': self.theme_var.get()
                        }
                        with open(file_path, 'w', encoding='utf-8') as f:
                            json.dump(data, f, ensure_ascii=False, indent=2)
                        messagebox.showinfo("Başarılı", "Harita kaydedildi.")
                    except Exception as e:
                        messagebox.showerror("Hata", f"Kayıt sırasında hata: {str(e)}")

    def load_mapping(self):
                file_path = filedialog.askopenfilename(
                    filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
                )
                if file_path:
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            data = json.load(f)
                        self.encryptor.char_positions = data['mapping']
                        if 'theme' in data:
                            self.theme_var.set(data['theme'])
                            self.change_theme()
                        self.circle_canvas.draw_circle()
                        messagebox.showinfo("Başarılı", "Harita yüklendi.")
                    except Exception as e:
                        messagebox.showerror("Hata", f"Yükleme sırasında hata: {str(e)}")

    def encrypt_text(self):
        text = self.input_text.get().strip()
        if not text:
            messagebox.showwarning("Uyarı", "Lütfen bir metin girin!")
            return

        encrypted = ""
        for char in text:
            if char in self.encryptor.char_positions:
                angle = self.encryptor.char_positions[char]
                region = int(angle // 90) + 1
                position = int(angle % 90)  # int'e çevirdik
                encrypted += f"{region}{position:02d}"

        self.output_text.delete(0, tk.END)
        self.output_text.insert(0, encrypted)

        # Animasyonu başlat
        self.circle_canvas.animate_encryption(text)

    def decrypt_text(self):
        encrypted = self.input_text.get().strip()
        if not encrypted or len(encrypted) % 3 != 0:
            messagebox.showwarning("Uyarı", "Geçersiz şifreli metin!")
            return

        decrypted = ""
        for i in range(0, len(encrypted), 3):
            region = int(encrypted[i])
            position = int(encrypted[i + 1:i + 3])
            angle = float(((region - 1) * 90) + position)  # float'a çevirdik

            # Bu açıdaki karakteri bul
            for char, char_angle in self.encryptor.char_positions.items():
                if abs(char_angle - angle) < 0.1:  # küçük bir tolerans ekledik
                    decrypted += char
                    break

        self.output_text.delete(0, tk.END)
        self.output_text.insert(0, decrypted)

    def clear_selection(self):
                self.circle_canvas.selected_chars = []
                self.selected_text.delete(0, tk.END)
                self.circle_canvas.draw_circle()

if __name__ == "__main__":
    app = EncryptionApp()
    app.mainloop()