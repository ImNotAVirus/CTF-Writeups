/*
** Credits: https://www.geeksforgeeks.org/quick-sort/
*/

#include <stdio.h>
#include <stdlib.h>

typedef unsigned long ulong;
typedef unsigned short ushort;
typedef unsigned int uint;

// A utility function to swap two elements
void swap(ushort* a, ushort* b)
{
    ushort t = *a;
    *a = *b;
    *b = t;
}

/* This function takes last element as pivot, places
   the pivot element at its correct position in sorted
    array, and places all smaller (smaller than pivot)
   to left of pivot and all greater elements to right
   of pivot */
int partition (ushort arr[], int low, int high)
{
    ushort pivot = arr[high];    // pivot
    int i = (low - 1);  // Index of smaller element

    for (int j = low; j <= high- 1; j++)
    {
        // If current element is smaller than or
        // equal to pivot
        if (arr[j] <= pivot)
        {
            i++;    // increment index of smaller element
            swap(&arr[i], &arr[j]);
        }
    }
    swap(&arr[i + 1], &arr[high]);
    return (i + 1);
}

/* The main function that implements QuickSort
 arr[] --> Array to be sorted,
  low  --> Starting index,
  high  --> Ending index */
void quick_sort(ushort arr[], int low, int high)
{
    if (low < high)
    {
        /* pi is partitioning index, arr[p] is now
           at right place */
        int pi = partition(arr, low, high);

        // Separately sort elements before
        // partition and after partition
        quick_sort(arr, low, pi - 1);
        quick_sort(arr, pi + 1, high);
    }
}

/*
** Quick sort wrapper !!
*/

void sort_array(ushort *new_array_half,int half_file_len)
{
    quick_sort(new_array_half, 0, half_file_len-1);
}
