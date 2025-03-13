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
    vector<int>data;
    for(int i = 0; i<size_of_vector; i++)
    {
        srand(time(0));
        int k = rand();
        k %=  max_size_of_number;
        data.push_back(k);
    }
    return data;
}


void heapify(vector<int>& arr, int n, int i) {
    int largest = i; // Inicjalizuj największy jako korzeń
    int left = 2 * i + 1; // lewy = 2*i + 1
    int right = 2 * i + 2; // prawy = 2*i + 2

    // Jeśli lewy liść jest większy niż korzeń
    if (left < n && arr[left] > arr[largest])
        largest = left;

    // Jeśli prawy liść jest większy niż największy dotychczasowy
    if (right < n && arr[right] > arr[largest])
        largest = right;

    // Jeśli największy nie jest korzeniem
    if (largest != i) {
        swap(arr[i], arr[largest]);

        // Rekurencyjnie heapify poddrzewo
        heapify(arr, n, largest);
    }
}

void heapSort(vector<int>& arr) {
    int n = arr.size();

    // Zbuduj kopiec (przekształć tablicę w kopiec)
    for (int i = n / 2 - 1; i >= 0; i--)
        heapify(arr, n, i);

    // Jeden po drugim wyciągaj elementy z kopca
    for (int i = n - 1; i >= 0; i--) {
        // Przenieś bieżący korzeń na koniec
        swap(arr[0], arr[i]);

        // Wywołaj heapify na zmniejszonym kopcu
        heapify(arr, i, 0);
    }
}

void testArray(){
    //~ Testing purposes -> 10 number array

    struct timeval begin, end;
    gettimeofday(&begin, 0);


    vector<int> arr = {12, 11, 13, 5, 6, 7, 4, 6, 2, 9, 43};
    int arr_size = arr.size();

    cout << "Before: " << endl;
    for (int i = 0; i < arr_size; i++)
        cout << arr[i] << " ";
    cout << endl;

    heapSort(arr);

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
    vector<int>unsorted = randomDataVector(99999, 1000);
    

    //* start timer 
    struct timeval begin, end;
    gettimeofday(&begin, 0);
    
    //^ sorting
    heapSort(unsorted);

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