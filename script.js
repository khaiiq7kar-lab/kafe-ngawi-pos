let dataBarang = [];
let total = 0;

const nama = document.getElementById("nama");
const harga = document.getElementById("harga");
const promo = document.getElementById("promo");
const struk = document.getElementById("struk");

function rupiah(angka) {
  return new Intl.NumberFormat("id-ID").format(angka);
}

function popup(title, message) {
  document.getElementById("popupTitle").textContent = title;
  document.getElementById("popupMessage").textContent = message;
  document.getElementById("popup").classList.remove("hidden");
}

function updateStruk() {
  if (dataBarang.length === 0) {
    struk.textContent = "Belum ada barang.";
    return;
  }

  let lines = ["STRUK BELANJA", ""];
  let subtotal = 0;

  dataBarang.forEach((barang, i) => {
    lines.push(`${i + 1}. ${barang.nama}  |  Rp ${rupiah(barang.harga)}`);
    subtotal += barang.harga;
  });

  lines.push("");
  lines.push(`SUBTOTAL: Rp ${rupiah(subtotal)}`);

  if (subtotal >= 50000) {
    lines.push("BONUS: Promo KAFENGAWI berlaku untuk diskon Rp 5.000.");
  }

  struk.textContent = lines.join("\n");
}

function tambahBarang() {
  const namaBarang = nama.value.trim();
  const hargaText = harga.value.trim();

  if (!namaBarang || !hargaText) {
    popup("Data belum lengkap", "Isi nama barang dan harga terlebih dahulu.");
    return;
  }

  const hargaBarang = Number(hargaText);

  if (!Number.isFinite(hargaBarang) || hargaBarang < 0) {
    popup("Harga tidak valid", "Masukkan harga yang benar.");
    return;
  }

  dataBarang.push({
    nama: namaBarang,
    harga: hargaBarang
  });

  nama.value = "";
  harga.value = "";
  updateStruk();
  nama.focus();
}

function hitung() {
  if (dataBarang.length === 0) {
    popup("Keranjang kosong", "Tambahkan barang dulu.");
    return;
  }

  let hasil = dataBarang.reduce((sum, barang) => sum + barang.harga, 0);
  const kode = promo.value.trim().toUpperCase();
  let pesan = "";

  if (kode === "KAFENGAWI") {
    if (hasil >= 50000) {
      hasil -= 5000;
      pesan = "Promo berhasil! Diskon Rp 5.000.";
    } else {
      pesan = "Promo hanya berlaku saat total belanja minimal Rp 50.000.";
    }
  } else if (kode) {
    pesan = "Kode promo salah atau sudah kadaluarsa.";
  }

  total = hasil;

  let lines = ["STRUK BELANJA", ""];

  dataBarang.forEach((barang, i) => {
    lines.push(`${i + 1}. ${barang.nama}  |  Rp ${rupiah(barang.harga)}`);
  });

  lines.push("");
  lines.push(`TOTAL: Rp ${rupiah(total)}`);

  if (pesan) {
    lines.push("");
    lines.push(pesan);
  }

  lines.push("");
  lines.push("Terimakasih sudah berbelanja!");

  struk.textContent = lines.join("\n");
}

function reset() {
  dataBarang = [];
  total = 0;
  nama.value = "";
  harga.value = "";
  promo.value = "";
  updateStruk();
}

document.getElementById("tambah").addEventListener("click", tambahBarang);
document.getElementById("hitung").addEventListener("click", hitung);
document.getElementById("pakaiPromo").addEventListener("click", hitung);
document.getElementById("reset").addEventListener("click", reset);

document.getElementById("popupClose").addEventListener("click", () => {
  document.getElementById("popup").classList.add("hidden");
});

harga.addEventListener("keydown", (e) => {
  if (e.key === "Enter") tambahBarang();
});

promo.addEventListener("keydown", (e) => {
  if (e.key === "Enter") hitung();
});

updateStruk();
