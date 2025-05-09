#include <iostream>
#include <vector>
#include <sys/time.h>

using namespace std;

int ctr = 0;
int swp = 0;

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


int podzial(vector<int>& tablica, int leftMarker, int rightMarker, bool a) {
    int pivot = tablica[rightMarker];
    if(a == true)
    {
        cout << pivot << endl;
    }

    int i = leftMarker - 1;

    for (int j = leftMarker; j < rightMarker; j++) {
        ctr++;
        if (tablica[j] < pivot) {
            i++;
            swap(tablica[i], tablica[j]);
            swp++;
        }
    }
    swap(tablica[i + 1], tablica[rightMarker]);
    swp++;
    return i + 1;
}

void quickSort(vector<int>& tablica, int leftMarker, int rightMarker, bool a) {
    ctr++;
    if (leftMarker < rightMarker) 
    {
        int pi = podzial(tablica, leftMarker, rightMarker, a);


        quickSort(tablica, leftMarker, pi - 1, a);
        quickSort(tablica, pi + 1, rightMarker, a);
    }
}

void testArray(){
    //~ Testing purposes -> 10 number array

    struct timeval begin, end;
    gettimeofday(&begin, 0);


    vector<int> arr = {12, 11, 13, 5, 6, 7, 4, 6, 2, 9, 43};
    int arr_size = arr.size();

    cout << "Before: " << endl << endl;
    for (int i = 0; i < arr_size; i++)
    {
        cout << arr[i] << " ";
    }
    cout << endl;

    quickSort(arr, 0, arr_size - 1, 1);

    cout << "After:"<<endl;
    for (int i = 0; i < arr_size; i++) 
    {
        cout << arr[i] << " ";
    }
    cout << endl;
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
    quickSort(unsorted, 0, unsorted.size() - 1, 0);

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
    cout << ctr << " " << swp << endl;
    main_task();
    return 0;
}