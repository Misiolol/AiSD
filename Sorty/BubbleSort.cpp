#include<iostream>
#include<vector>
#include<fstream>


using namespace std;

// Funkcja do wypisywania wektora
void WypiszWektor(vector<int> &wektor)
{
    cout << "Wektor: " << endl;
    for(int i = 0; i < wektor.size(); i++)
    {
        cout << wektor[i] << " ";
    }
    cout << endl;
}

// Procedura losujaca dane
vector<int> generateRandomVector(int size, int maxValue) {
    vector<int> randomVector;
    randomVector.reserve(size); // Rezerwujemy miejsce na elementy

    // Inicjalizujemy generator liczb losowych
    srand(static_cast<unsigned int>(time(0))); 

    // Wypełniamy vector losowymi liczbami
    for (int i = 0; i < size; ++i) {
        randomVector.push_back(std::rand() % (maxValue + 1)); // Losujemy liczbę od 0 do maxValue
    }

   

    return randomVector;
}


void zapiszDoPliku(int liczbaPorownan, int liczbaZamian)
{
    // Otwieramy plik w trybie dopisywania (ios::app)
    ofstream plik("statystyki_sortowania.txt", ios::app);
    
    // Sprawdzamy, czy plik został otwarty poprawnie
    if (!plik.is_open())
    {
        cout << "Nie można otworzyć pliku!" << endl;
        return;
    }

    // Zapisujemy liczby porównań i zamian
    plik << "Liczba porównań: " << liczbaPorownan << endl;
    plik << "Liczba zamian: " << liczbaZamian << endl;
    
    // Zamykamy plik
    plik.close();
}



vector<int> SortowanieBabelkowe(vector<int> &tablica)
{
    int rozmiar = tablica.size();
    int liczbaPorownan = 0;  // Liczba porównań
    int liczbaZamian = 0;    // Liczba zamian

    for (int i = 0; i < rozmiar - 1; i++)
    {
        // Inicjalizacja indeksu minimalnego
        int indeksMin = i;
        for (int j = i + 1; j < rozmiar; j++)
        {
            // Znalezienie minimalnego elementu w nieposortowanej części
            liczbaPorownan++;  // Zwiększamy liczbę porównań
            if (tablica[j] < tablica[indeksMin])
            {
                indeksMin = j;
            }
        }
        // Zamiana znalezionego minimalnego elementu z pierwszym elementem
        if (indeksMin != i) {
            swap(tablica[i], tablica[indeksMin]);
            liczbaZamian++;  // Zwiększamy liczbę zamian
        }
    }

    // Po zakończeniu sortowania zapisujemy statystyki do pliku
    zapiszDoPliku(liczbaPorownan, liczbaZamian);

    return tablica;
}

void testArray(){
    //~ Testing purposes -> 10 number array




    vector<int> arr = {12, 11, 13, 5, 6, 7, 4, 6, 2, 9, 43};
    int arr_size = arr.size();

    cout << "Before: " << endl;
    for (int i = 0; i < arr_size; i++)
        cout << arr[i] << " ";
    cout << endl;

    SortowanieBabelkowe(arr);

    cout << "After:"<<endl;
    for (int i = 0; i < arr_size; i++)
        cout << arr[i] << " ";
    cout << endl;

}


void main_task(int a){
    //! generating random data array
    vector<int>unsorted = generateRandomVector(a, a*10);
    
    for(int i = 0; i < unsorted.size(); i++)
    {
        cout << unsorted[i] << " ";
    }

    SortowanieBabelkowe(unsorted);


}

int main()
{
    main_task(10);
    main_task(100);
    main_task(400);
    main_task(800);
    main_task(1000);
    main_task(4000);
    main_task(8000);
    main_task(10000);
    main_task(40000);
    main_task(80000);
    main_task(100000);
}