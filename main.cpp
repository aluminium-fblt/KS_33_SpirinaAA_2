#include <iostream>
#include <vector>
#include <random>
#include <chrono>
#include <fstream>
#include <future>
#include <mutex>

using namespace std;

struct Result {
    double time_sec;
    long long passes;   // повторные прохождения
    long long swaps;    // операции обмена
};

// СОРТИРОВКА ВСТАВКАМИ
Result insertionSort(vector<double>& arr)
{
    long long passes = 0;
    long long swaps = 0;

    auto start = chrono::high_resolution_clock::now();

    for (size_t i = 1; i < arr.size(); ++i)
    {
        passes++;  // одно прохождение

        double key = arr[i];
        int j = i - 1;

        while (j >= 0 && arr[j] > key)
        {
            arr[j + 1] = arr[j];
            swaps++;
            j--;
        }

        arr[j + 1] = key;
    }

    auto end = chrono::high_resolution_clock::now();
    chrono::duration<double> diff = end - start;

    return { diff.count(), passes, swaps };
}

// ГЛОБАЛЬНЫЙ МЬЮТЕКС
mutex file_mutex;

// ОДНА СЕРИЯ
void run_series(int series,
                const vector<int>& sizes,
                ofstream& file)
{
    mt19937 engine(random_device{}());
    uniform_real_distribution<double> gen(-1.0, 1.0);

    for (int n : sizes)
    {
        for (int run = 1; run <= 20; run++)
        {
            vector<double> arr(n);

            for (auto& el : arr)
                el = gen(engine);

            Result r = insertionSort(arr);

            // потокобезопасная запись
            {
                lock_guard<mutex> lock(file_mutex);

                file << series << ","
                     << run << ","
                     << n << ","
                     << r.time_sec << ","
                     << r.passes << ","
                     << r.swaps << "\n";
            }
        }
    }
}

int main()
{
    vector<int> sizes = {1000, 2000, 4000, 8000,
                         16000, 32000, 64000, 128000};

    ofstream file("results.csv");
    file << "series,run,size,time_sec,passes,swaps\n";

    vector<future<void>> futures;

    // Запускаем 8 серий параллельно (8 потоков)
    for (int series = 1; series <= 8; series++)
    {
        futures.push_back(
                async(launch::async,
                      run_series,
                      series,
                      cref(sizes),
                      ref(file))
        );
    }

    // Ждём завершения всех потоков
    for (auto& f : futures)
        f.get();

    file.close();

    cout << "Все серии завершены. Данные сохранены в results.csv\n";

    return 0;
}
