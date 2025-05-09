#include <iostream>
#include <vector>
#include <sys/time.h>

using namespace std;


int swp = 0;
int ctr = 0;

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

void selectionSort(vector<int>& arr) 
{
    int n = arr.size();
    for (int i = 0; i < n - 1; i++) 
    {
        int minIndex = i;
        for (int j = i + 1; j < n; j++) 
        {
            ctr++;
            if (arr[j] < arr[minIndex]) 
            {
                minIndex = j;
            }
        }
        swap(arr[i], arr[minIndex]);
        swp++;
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

    selectionSort(arr);

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
    selectionSort(unsorted);

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