# Observer Pattern

The Observer pattern is a behavioral design pattern where an object, known as the subject, 
maintains a list of dependents, called observers, that are notified of any changes in the subject's state. 
This pattern establishes a one-to-many relationship between objects, where multiple observers can listen to and respond to changes in the subject without being tightly coupled to it. 
This decoupling promotes flexibility and reusability in the design of software systems.

The Observer pattern allows for dynamic relationships between objects. Observers can be added or removed at runtime, enabling flexibility in how objects collaborate. This pattern is widely used in various scenarios, 
including implementing graphical user interfaces, event handling systems, and distributed systems.

### Example

```cpp
#include <algorithm>
#include <iostream>
#include <vector>

// Observer interface that defines the update method to be called by the subject.
class Observer {
public:
    virtual ~Observer() = default;
    virtual void update(int newState) = 0;
};

// Subject interface that defines methods for attaching, detaching, and notifying observers.
class Subject {
public:
    virtual ~Subject() = default;
    virtual void attach(Observer* observer) = 0;
    virtual void detach(Observer* observer) = 0;
    virtual void notify() = 0;
};

// Concrete subject class that implements the Subject interface.
class ConcreteSubject : public Subject {
public:
    void attach(Observer* observer) override {
        observers_.emplace_back(observer);
    }

    void detach(Observer* observer) override {
        observers_.erase(
            std::remove(observers_.begin(), observers_.end(), observer),
            observers_.end());
    }

    void setState(int state) {
        state_ = state;
        notify(); // Notify observers when the state changes.
    }

    int getState() const {
        return state_;
    }

    void notify() override {
        for (Observer* observer : observers_) {
            observer->update(state_);
        }
    }

private:
    std::vector<Observer*> observers_;
    int state_ = 0;
};

// Concrete observer class that implements the Observer interface.
class ConcreteObserver : public Observer {
public:
    ConcreteObserver(ConcreteSubject* subject) : subject_(subject) {
        subject_->attach(this);
    }

    ~ConcreteObserver() override {
        subject_->detach(this);
    }

    void update(int newState) override {
        std::cout << "Observer received update. New state: " << newState << std::endl;
    }

private:
    ConcreteSubject* subject_;
};

int main() {
    ConcreteSubject subject;

    ConcreteObserver observer1(&subject);
    ConcreteObserver observer2(&subject);

    // Change the state of the subject, which triggers the notification to observers.
    subject.setState(42);

    return 0;
}
```

In this example, `Subject` is an interface that declares methods for attaching, 
detaching, and notifying observers. ConcreteSubject is a class implementing the Subject interface. 
It maintains a list of observers and notifies them when its state changes.

`Observer` is an interface with an `update` method that concrete observers must implement. 
`ConcreteObserver` is a class implementing the `Observer`. It registers itself with a 
`ConcreteSubject` instance and receives updates when the subject's state changes.

In the main function, a `ConcreteSubject` instance is created, and two `ConcreteObserver` 
instances are attached to it. When the subject's state changes using `subject.setState(42)`, 
both observers are notified, and they print the new state.
