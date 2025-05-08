#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

// Funkcja implementująca sortowanie Shella
void shellSort(vector<int>& a) {
    int N = a.size(); // Pobranie rozmiaru wektora
    int h = 1; // Inicjalizacja odstępu (h-gap)
    
    // Obliczanie maksymalnego odstępu h według formuły Knutha: h = 3*h + 1
    while (h < N / 3) {
        h = 3 * h + 1;
    }
    
    // Główna pętla sortowania Shella
    while (h >= 1) { 
        // Sortowanie przez wstawianie z odstępem h
        for (int i = h; i < N; i++) {
            // Przesuwanie elementów w podtablicach o odstępie h
            for (int j = i; j >= h && a[j] < a[j - h]; j -= h) {
                swap(a[j], a[j - h]); // Zamiana elementów
            }
        }
        
        // Po każdej iteracji zmniejszamy odstęp h
        h = h / 3;

        // Wypisanie tablicy po każdej iteracji, aby zobaczyć proces sortowania
        for (int num : a) {
            cout << num << " ";
        }
        cout << endl;
    }
}

// Funkcja główna programu
int main() {
    vector<int> a = {16, 80, 51, 9, 23, 51, 65, 40, 80, 17}; // Przykładowa tablica do posortowania
    shellSort(a); // Wywołanie funkcji sortującej
    return 0; // Zakończenie programu
}
