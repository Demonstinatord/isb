#include <iostream>
#include <random>
//#include <bitset>
#include <fstream>



int main() {
    setlocale(LC_ALL, ""); // ��������� ������ ��� ����������� ����������� �������� ������

    std::mt19937 gen(std::random_device{}()); // ��������� Mersenne Twister
    std::uniform_int_distribution<> dis(0, 1); // ����������� �������������: 0 ��� 1

    std::ofstream outfile("I:/semi4 labs/isb/isb_lab2/random_numbers/sequence_c++.txt");


    for (int i = 0; i < 128; ++i) {
        int bit = dis(gen);
        outfile << bit;
        std::cout << bit;
    }
    std::cout << "\n";
    outfile.close();

    std::cout << "�������� ������������������ ������ 128 ��� �������� � ���� sequence_c++.txt\n";

    return 0;
}