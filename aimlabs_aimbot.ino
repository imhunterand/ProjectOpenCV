#include <Mouse.h>
int tombolPin = 9;  // Tetapkan tombol ke pin apa saja

void setup() {
  Serial.begin(115200);
  Serial.setTimeout(1);
  // pinMode(tombolPin, INPUT);  // Atur tombol sebagai input
  digitalWrite(tombolPin, HIGH);  // Tahan tombol tinggi
  delay(1000);  // Delay pendek untuk membiarkan keluaran stabil
  Mouse.begin(); //Mulai emulasi mouse
}

void loop() {
  if (Serial.available() > 0) {
    String masukan = Serial.readStringUntil('\n'); // Baca input serial hingga karakter baris baru
    masukan.trim(); // Hapus spasi awal dan akhir
    //Serial.println(masukan);
    // Periksa apakah input valid
    if (masukan == "kiri") {
        Mouse.click(MOUSE_LEFT);
      }
      if (masukan == "kanan") {
        Mouse.click(MOUSE_RIGHT);
      }
      else
      {
    //if (masukan.startsWith("[") && masukan.endsWith("]")) {
      masukan.remove(0, 1); // Hapus tanda kurung awal
      masukan.remove(masukan.length() - 1); // Hapus tanda kurung akhir
      //Serial.println(masukan);
      char arrayKarakter[masukan.length() + 1];
      
      masukan.toCharArray(arrayKarakter, sizeof(arrayKarakter));
      //Serial.println("array karakter");
      //Serial.println(arrayKarakter);
      char *pasangan = strtok(arrayKarakter, ", ");
      //Serial.println(pasangan);
      while (pasangan != NULL) {
        String pasanganStr = pasangan;
        //Serial.println(pasangan);
        //pasanganStr.trim();
        pasanganStr.remove(0, 1); // Hapus tanda kurung awal
        pasanganStr.remove(pasanganStr.length() - 1); // Hapus tanda kurung akhir

        int indeksKoma = pasanganStr.indexOf(":");
        if (indeksKoma != -1) {
          String xStr = pasanganStr.substring(0, indeksKoma);
          String yStr = pasanganStr.substring(indeksKoma + 1);

          int x = xStr.toInt();
          int y = yStr.toInt();
          //Serial.println(x);
          //Serial.println(y);
          float lim = (float)1 + ((float)100/(float)254);
          //Serial.println(lim);
          // Gerakkan mouse ke koordinat yang ditentukan
          int finx = round((float)x * (float)lim); // Atur untuk batasan 127 arduino
          int finy = round((float)y * (float)lim); // Atur untuk batasan 127 arduino
          //Serial.println(finx);
          //Serial.println(finy);
          Mouse.move(finx, finy, 0);

          //delay(1); // Tambahkan delay untuk mencegah gerakan cepat
        }

        pasangan = strtok(NULL, ", ");
      }
    }
  }
  Serial.flush();
  //Serial.End();
  //Serial.begin(115200);
  }
