from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.metrics import dp
from kivy.core.window import Window


class KasirPOS(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", padding=dp(12), spacing=dp(8), **kwargs)
        self.data_barang = []

        self.add_widget(Label(
            text="[b]KAFE NGAWI[/b]\\nSISTEM KASIR POS",
            markup=True, font_size=dp(24), size_hint_y=None, height=dp(70)
        ))

        form = GridLayout(cols=2, spacing=dp(8), size_hint_y=None, height=dp(100))
        form.add_widget(Label(text="Nama barang:", halign="left"))
        self.nama = TextInput(multiline=False, hint_text="Contoh: Kopi")
        form.add_widget(self.nama)
        form.add_widget(Label(text="Harga:", halign="left"))
        self.harga = TextInput(multiline=False, input_filter="int", hint_text="Contoh: 15000")
        form.add_widget(self.harga)
        self.add_widget(form)

        tombol = BoxLayout(size_hint_y=None, height=dp(48), spacing=dp(8))
        tambah = Button(text="TAMBAH BARANG")
        tambah.bind(on_press=self.tambah_barang)
        selesai = Button(text="SELESAI / HITUNG")
        selesai.bind(on_press=self.hitung)
        tombol.add_widget(tambah)
        tombol.add_widget(selesai)
        self.add_widget(tombol)

        self.struk = Label(
            text="Belum ada barang.",
            halign="left", valign="top", size_hint_y=None
        )
        self.struk.bind(texture_size=lambda obj, val: setattr(obj, "height", val[1]))
        scroll = ScrollView()
        scroll.add_widget(self.struk)
        self.add_widget(scroll)

        promo_box = BoxLayout(size_hint_y=None, height=dp(48), spacing=dp(8))
        self.promo = TextInput(multiline=False, hint_text="Kode promo (opsional)")
        promo_btn = Button(text="PAKAI PROMO", size_hint_x=None, width=dp(130))
        promo_btn.bind(on_press=self.hitung)
        promo_box.add_widget(self.promo)
        promo_box.add_widget(promo_btn)
        self.add_widget(promo_box)

        bawah = BoxLayout(size_hint_y=None, height=dp(50), spacing=dp(8))
        reset = Button(text="RESET")
        reset.bind(on_press=self.reset)
        keluar = Button(text="KELUAR")
        keluar.bind(on_press=lambda *_: App.get_running_app().stop())
        bawah.add_widget(reset)
        bawah.add_widget(keluar)
        self.add_widget(bawah)

        self.total = 0
        self.update_struk()

    def tambah_barang(self, *_):
        nama = self.nama.text.strip()
        harga_text = self.harga.text.strip()

        if not nama or not harga_text:
            self.popup("Data belum lengkap", "Isi nama barang dan harga terlebih dahulu.")
            return

        harga = int(harga_text)
        self.data_barang.append({"nama": nama, "harga": harga})
        self.nama.text = ""
        self.harga.text = ""
        self.update_struk()

    def update_struk(self):
        if not self.data_barang:
            self.struk.text = "Belum ada barang."
            return

        lines = ["[b]STRUK BELANJA[/b]", ""]
        total = 0
        for i, barang in enumerate(self.data_barang, 1):
            lines.append(f"{i}. {barang['nama']}  |  Rp {barang['harga']:,}".replace(",", "."))
            total += barang["harga"]

        lines += ["", f"[b]SUBTOTAL: Rp {total:,}[/b]".replace(",", ".")]
        if total >= 50000:
            lines.append("BONUS: Promo KAFENGAWI berlaku untuk diskon Rp 5.000.")
        self.struk.text = "\n".join(lines)
        self.struk.markup = True

    def hitung(self, *_):
        if not self.data_barang:
            self.popup("Keranjang kosong", "Tambahkan barang dulu.")
            return

        total = sum(x["harga"] for x in self.data_barang)
        promo = self.promo.text.strip().upper()

        pesan = ""
        if promo == "KAFENGAWI":
            if total >= 50000:
                total -= 5000
                pesan = "Promo berhasil! Diskon Rp 5.000."
            else:
                pesan = "Promo hanya berlaku saat total belanja minimal Rp 50.000."
        elif promo:
            pesan = "Kode promo salah atau sudah kadaluarsa."

        self.total = total
        lines = ["[b]STRUK BELANJA[/b]", ""]
        for i, barang in enumerate(self.data_barang, 1):
            lines.append(f"{i}. {barang['nama']}  |  Rp {barang['harga']:,}".replace(",", "."))
        lines += ["", f"[b]TOTAL: Rp {total:,}[/b]".replace(",", ".")]
        if pesan:
            lines += ["", pesan]
        lines += ["", "Terimakasih sudah berbelanja!"]
        self.struk.text = "\n".join(lines)
        self.struk.markup = True

    def reset(self, *_):
        self.data_barang.clear()
        self.promo.text = ""
        self.nama.text = ""
        self.harga.text = ""
        self.total = 0
        self.update_struk()

    def popup(self, title, message):
        Popup(
            title=title,
            content=Label(text=message),
            size_hint=(0.85, 0.35)
        ).open()


class KafeNgawiApp(App):
    title = "KAFE NGAWI POS"

    def build(self):
        Window.softinput_mode = "below_target"
        return KasirPOS()


if __name__ == "__main__":
    KafeNgawiApp().run()
