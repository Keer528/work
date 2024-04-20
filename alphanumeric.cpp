#include <iostream>
#include <pthread.h>
#include <vector>
#include <string>
#include <sstream> // Include stringstream for splitting the input phrase
#include <cstdlib>
#include <cctype>

using namespace std;

// Global variable to store the input phrase
string inputPhrase;

// Function to check if a character is a digit
bool isDigit(char c) {
    return isdigit(c);
}

// Function to check if a character is an alphabet
bool isAlpha(char c) {
    return isalpha(c);
}

// Function to print words that begin with an alphabet
void *alpha(void *arg) {
    string threadName = "alpha";
    stringstream ss(inputPhrase); // Create a stringstream from the input phrase
    string word;
    while (ss >> word) { // Extract words from stringstream
        if (!word.empty() && isAlpha(word[0])) {
            cout << threadName << ": " << word << endl;
        }
    }
    pthread_exit(NULL);
}

// Function to print words that begin with a number
void *numeric(void *arg) {
    string threadName = "numeric";
    stringstream ss(inputPhrase); // Create a stringstream from the input phrase
    string word;
    while (ss >> word) { // Extract words from stringstream
        if (!word.empty() && isDigit(word[0])) {
            cout << threadName << ": " << word << endl;
        }
    }
    pthread_exit(NULL);
}

int main(int argc, char *argv[]) {
    // Check if phrase is provided as command line argument
    if (argc == 2) {
        inputPhrase = argv[1];
    } else {
        // Prompt for input phrase
        cout << "Enter string: ";
        getline(cin, inputPhrase);
    }

    pthread_t alphaThread, numericThread;
    int alphaThreadCreate, numericThreadCreate;

    // Create alpha thread
    alphaThreadCreate = pthread_create(&alphaThread, NULL, alpha, NULL);
    if (alphaThreadCreate) {
        cerr << "Error creating alpha thread" << endl;
        exit(-1);
    }

    // Create numeric thread
    numericThreadCreate = pthread_create(&numericThread, NULL, numeric, NULL);
    if (numericThreadCreate) {
        cerr << "Error creating numeric thread" << endl;
        exit(-1);
    }

    // Join alpha thread
    pthread_join(alphaThread, NULL);

    // Join numeric thread
    pthread_join(numericThread, NULL);

    return 0;
}
