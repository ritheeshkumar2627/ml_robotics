#include <iostream>
#include <vector>
#include <stdexcept>
#include<mutex>
#include <thread>

std::mutex mtx;
class CircularBuffer {
private:
    std::vector<double> buffer; // Fixed-size memory storage block
    int head;                   // Index pointer to the oldest item
    int tail;                   // Index pointer where the next item drops in
    int current_size;           // Tracks active elements in buffer
    int capacity;               // Maximum memory allocation ceiling

public:
    // Constructor allocating direct hardware block sizing
    CircularBuffer(int cap) {
        capacity = cap;
        buffer.resize(capacity, 0.0);
        head = 0;
        tail = 0;
        current_size = 0;
    }

    // Enqueue operation: Absolute zero-allocation O(1) time complexity
    void push(double item) {
        std::lock_guard<std::mutex> lock(mtx); // Thread-safe lock for concurrent access

        buffer[tail] = item;
        tail = (tail + 1) % capacity; // Cyclic increment wraparound math

        if (current_size == capacity) {
            // Buffer Overflow Safety Trap: Overwrite oldest value and advance head
            head = (head + 1) % capacity;
        } else {
            current_size++;
        }
    }

    // Dequeue operation: Absolute zero-allocation O(1) time complexity
    double pop() {
        std::lock_guard<std::mutex> lock(mtx); // Thread-safe lock for concurrent access

        if (current_size == 0) {
            throw std::underflow_error("❌ Queue Telemetry Underflow Error: Buffer Empty.");
        }

        double extracted_item = buffer[head];
        head = (head + 1) % capacity; // Cyclic increment wraparound math
        current_size--;
        return extracted_item;
    }

    int size() const { return current_size; }
    bool is_full() const { return current_size == capacity; }
};

int main() {
    std::cout << "⚙️ Initializing High-Frequency C++ Ring Buffer Test...\n";

    // Allocate an explicit 3-slot telemetry buffer queue
    CircularBuffer telemetry_queue(3);

    // Push 4 metrics continuously to force an intentional array overflow condition
    telemetry_queue.push(10.1);
    telemetry_queue.push(20.2);
    telemetry_queue.push(30.3);
    telemetry_queue.push(40.4); // Overwrites 10.1 and moves head pointer forward

    std::cout << "📦 Buffer current size (Expected: 3): " << telemetry_queue.size() << "\n";
    std::cout << "📥 Popping data element (Expected: 20.2): " << telemetry_queue.pop() << "\n";
    std::cout << "📥 Popping data element (Expected: 30.3): " << telemetry_queue.pop() << "\n";
    std::cout << "📥 Popping data element (Expected: 40.4): " << telemetry_queue.pop() << "\n";

    return 0;
}
