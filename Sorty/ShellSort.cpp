#include<iostream>
#include<vector>

using namespace std;

vector<int> shellsort(vector<int> data)
{
    int h = 1;
    int n = data.size();
    while (h < n / 3)
    {
        h = 3 * h + 1;
    }

    while (h > 0)
    {
        for (int j = h; j < n; j++)
        {
            int x = data[j];
            int i = j;
            while (i >= h && data[i - h] > x)
            {
                data[i] = data[i - h];
                i -= h;
            }
            data[i] = x;
        }
        h /= 3;
    }
    return data;
}

void VectorPrint(vector<int> a)
{
    for (int i = 0; i < a.size(); i++)
    {
        cout << a[i] << " ";
    }
    cout << endl;
}

int main()
{
    vector<int> dataset = {3, 5, 1, 7, 2, 4, 5};
    VectorPrint(shellsort(dataset)); // printing the result from already done function
}