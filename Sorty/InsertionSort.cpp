#include <iostream>
#include <vector>
#include <sys/time.h>

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
vector<int> randomDataVector(int size_of_vector, int max_size_of_number)
{
    vector<int> data;
    srand(time(0)); // Seed the random number generator once
    for (int i = 0; i < size_of_vector; i++)
    {
        int k = rand() % max_size_of_number;
        data.push_back(k);
    }
    return data;
}


void insertionSort(vector<int>& tablica) {
    int ctr = 0;
    int swp = 0;
    
    int rozmiar = tablica.size();
    for (int i = 1; i < rozmiar; ++i) {
        int klucz = tablica[i];
        int j = i - 1;
        while (j >= 0 && tablica[j] > klucz) {
            ctr+=2;
            tablica[j + 1] = tablica[j];
            swp++;
            j--;
        }
        tablica[j + 1] = klucz;
    }

    
    cout << ctr << endl;
    cout << swp << endl;
}


void testArray(){
    //~ Testing purposes -> 10 number array

    struct timeval begin, end;
    gettimeofday(&begin, 0);


    vector<int> arr = {12, 11, 13, 5, 6, 7, 4, 6, 2, 9, 43};
    int arr_size = arr.size();

    cout << "Before: " << endl << endl;
    for (int i = 0; i < arr_size; i++)
        cout << arr[i] << " ";
    cout << endl;

    insertionSort(arr);

    cout << "After:"<<endl;
    for (int i = 0; i < arr_size; i++)
        cout << arr[i] << " ";
    cout << endl;

    gettimeofday(&end, 0);
    long seconds = end.tv_sec - begin.tv_sec;
    long microseconds = end.tv_usec - begin.tv_usec;
    double elapsed = seconds + microseconds*1e-6;
    cout << elapsed << endl;
}

void main_task(){
    //! generating random data array
    vector<int>unsorted = randomDataVector(1000, 1000);

    //WypiszWektor(unsorted);
    

    //* start timer 
    struct timeval begin, end;
    gettimeofday(&begin, 0);
    
    //^ sorting
    insertionSort(unsorted);

    //* end timer
    gettimeofday(&end, 0);
    long seconds = end.tv_sec - begin.tv_sec;
    long microseconds = end.tv_usec - begin.tv_usec;
    double elapsed = seconds + microseconds*1e-6;
    
    cout << elapsed << endl;
}

int main() {
    ios_base::sync_with_stdio(0); 
    cin.tie(0);
    cout.tie(0);
    
    testArray();


    main_task();


    return 0;
}
