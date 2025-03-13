#include <iostream>
#include <vector>
#include <sys/time.h>

using namespace std;

void merge(vector<int>& arr, int left, int mid, int right) {
    int n1 = mid - left + 1;
    int n2 = right - mid;

    vector<int> L(n1), R(n2);

    for (int i = 0; i < n1; ++i)
        L[i] = arr[left + i];
    for (int j = 0; j < n2; ++j)
        R[j] = arr[mid + 1 + j];

    int i = 0, j = 0, k = left;
    while (i < n1 && j < n2) {
        if (L[i] <= R[j]) {
            arr[k] = L[i];
            ++i;
        } else {
            arr[k] = R[j];
            ++j;
        }
        ++k;
    }

    while (i < n1) {
        arr[k] = L[i];
        ++i;
        ++k;
    }

    while (j < n2) {
        arr[k] = R[j];
        ++j;
        ++k;
    }
}

void mergeSort(vector<int>& arr, int left, int right) {
    if (left < right) {
        int mid = left + (right - left) / 2;

        mergeSort(arr, left, mid);
        mergeSort(arr, mid + 1, right);

        merge(arr, left, mid, right);
    }
}

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

    mergeSort(arr, 0, arr_size - 1);

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
    vector<int>unsorted = randomDataVector(9999999, 1000);
    

    //* start timer 
    struct timeval begin, end;
    gettimeofday(&begin, 0);
    
    //^ sorting
    mergeSort(unsorted, 0, unsorted.size() - 1);

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
    
    
    
    //testArray();
    for(int i = 0; i<10; i++)
    {
        main_task();
    }
    return 0;
}