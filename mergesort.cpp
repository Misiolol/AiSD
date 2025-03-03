#include<iostream>
#include<vector>

using namespace std;


void PrintVec(vector<int>a)
{
    cout << "Vector: " << endl;
    for(int i = 0; i<a.size(); i++)
    {
        cout << a[i] << " ";
    }
}

void BubbleSort(vector<int>arr)
{
    int n = arr.size();
    for (int i = 0; i < n - 1; i++)
    {
        int minIndex = i;
        for (int j = i + 1; j < n; j++)
        {
            if (arr[j] < arr[minIndex])
            {
                minIndex = j;
            }
        }
        swap(arr[i], arr[minIndex]);
    }

    PrintVec(arr);
}


int main()
{
    int a;
    vector<int>arr;

    cin >> a;
    for(int i = 0; i<a; i++)
    {
        int k;
        cin >> k;
        arr.push_back(k);
    }
    
    BubbleSort(arr);
}