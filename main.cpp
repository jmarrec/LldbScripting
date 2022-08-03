#include <iostream>
#include <string>
#include <vector>

int main() {
  std::vector<std::string> vec{"First string", "Second String that is longer"};
  std::vector<int> intVec;
  intVec.resize(vec.size(), -1);
  std::vector<bool> moved;
  moved.resize(vec.size(), false);

  int newPos = 0;
  for (int i = 0; auto& s : vec) {
    if (s.size() > 20) {
      moved[i] = true;
      intVec[newPos++] = i;
    }
    ++i;
  }

  for (int i = 0; auto& s : vec) {
    if (!moved[i]) {
      moved[i] = true;
      intVec[newPos++] = i;
    }
    ++i;
  }

  for (auto i : intVec) {
    std::cout << i << " ";
  }
  std::cout << '\n';
}
