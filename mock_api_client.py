from dataclasses import dataclass
from typing import Any, Optional
import logging

# Настройка логирования
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('mock_api')

@dataclass
class ModelResponse:
    generated_text: str
    raw_response: Any
    status: bool
    error: Optional[str] = None

MOCK_RESPONSES = {
    "python": {
        "qwen": """Here's an implementation of bubble sort in Python:

```python
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        swapped = False
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
                swapped = True
        if not swapped:
            break
    return arr

# Example usage
numbers = [64, 34, 25, 12, 22, 11, 90]
sorted_numbers = bubble_sort(numbers.copy())
print(f"Original: {numbers}")
print(f"Sorted: {sorted_numbers}")
```

Key points:
1. Time complexity: O(n²)
2. Space complexity: O(1)
3. Adaptive: Yes
4. Stable: Yes""",
        "starcoder": """Here's a Python implementation of bubble sort with optimization:

```python
def optimized_bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        already_sorted = True
        for j in range(n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                already_sorted = False
        if already_sorted:
            break
    return arr

# Test the function
test_array = [64, 34, 25, 12, 22, 11, 90]
print("Before:", test_array)
sorted_array = optimized_bubble_sort(test_array.copy())
print("After:", sorted_array)
```

Features:
1. Early termination
2. In-place sorting
3. Simple implementation
4. Good for small datasets"""},
    "javascript": {
        "qwen": """Here's a JavaScript implementation of bubble sort:

```javascript
function bubbleSort(arr) {
    const n = arr.length;
    
    for (let i = 0; i < n; i++) {
        let swapped = false;
        
        for (let j = 0; j < n - i - 1; j++) {
            if (arr[j] > arr[j + 1]) {
                [arr[j], arr[j + 1]] = [arr[j + 1], arr[j]];
                swapped = true;
            }
        }
        
        if (!swapped) break;
    }
    
    return arr;
}

// Example usage
const numbers = [64, 34, 25, 12, 22, 11, 90];
console.log('Original:', numbers);
console.log('Sorted:', bubbleSort([...numbers]));
```

Key features:
1. Uses ES6+ syntax
2. In-place sorting
3. Early termination optimization
4. Array destructuring for swaps""",
        "starcoder": """Here's an optimized JavaScript bubble sort implementation:

```javascript
function optimizedBubbleSort(arr) {
    let start = 0;
    let end = arr.length - 1;
    let swapped;

    while (start < end) {
        swapped = false;
        
        for (let i = start; i < end; i++) {
            if (arr[i] > arr[i + 1]) {
                [arr[i], arr[i + 1]] = [arr[i + 1], arr[i]];
                swapped = true;
            }
        }
        
        if (!swapped) break;
        end--;
        
        for (let i = end - 1; i >= start; i--) {
            if (arr[i] > arr[i + 1]) {
                [arr[i], arr[i + 1]] = [arr[i + 1], arr[i]];
                swapped = true;
            }
        }
        
        start++;
    }
    
    return arr;
}

// Test the function
const testArray = [64, 34, 25, 12, 22, 11, 90];
console.log('Before:', testArray);
console.log('After:', optimizedBubbleSort([...testArray]));
```

Improvements:
1. Bidirectional bubbling
2. Early termination
3. Optimized range reduction
4. Modern JS features"""},
    "cpp": {
        "qwen": """Here's a C++ implementation of bubble sort:

```cpp
#include <iostream>
#include <vector>

void bubbleSort(std::vector<int>& arr) {
    int n = arr.size();
    bool swapped;
    
    for (int i = 0; i < n; i++) {
        swapped = false;
        
        for (int j = 0; j < n - i - 1; j++) {
            if (arr[j] > arr[j + 1]) {
                std::swap(arr[j], arr[j + 1]);
                swapped = true;
            }
        }
        
        if (!swapped) break;
    }
}

int main() {
    std::vector<int> numbers = {64, 34, 25, 12, 22, 11, 90};
    
    std::cout << "Original array: ";
    for (int num : numbers) std::cout << num << " ";
    std::cout << std::endl;
    
    bubbleSort(numbers);
    
    std::cout << "Sorted array: ";
    for (int num : numbers) std::cout << num << " ";
    std::cout << std::endl;
    
    return 0;
}
```

Features:
1. Uses STL vector
2. Modern C++ syntax
3. Early termination
4. Pass by reference for efficiency""",
        "starcoder": """Here's an optimized C++ bubble sort implementation:

```cpp
#include <iostream>
#include <vector>
#include <algorithm>

template<typename T>
void optimizedBubbleSort(std::vector<T>& arr) {
    int n = arr.size();
    int start = 0;
    int end = n - 1;
    bool swapped;
    
    while (start < end) {
        swapped = false;
        
        for (int i = start; i < end; i++) {
            if (arr[i] > arr[i + 1]) {
                std::swap(arr[i], arr[i + 1]);
                swapped = true;
            }
        }
        
        if (!swapped) break;
        end--;
        
        for (int i = end - 1; i >= start; i--) {
            if (arr[i] > arr[i + 1]) {
                std::swap(arr[i], arr[i + 1]);
                swapped = true;
            }
        }
        
        start++;
    }
}

int main() {
    std::vector<int> numbers = {64, 34, 25, 12, 22, 11, 90};
    
    std::cout << "Before sorting: ";
    for (const auto& num : numbers) std::cout << num << " ";
    std::cout << std::endl;
    
    optimizedBubbleSort(numbers);
    
    std::cout << "After sorting: ";
    for (const auto& num : numbers) std::cout << num << " ";
    std::cout << std::endl;
    
    return 0;
}
```

Advanced features:
1. Template implementation
2. Bidirectional bubbling
3. Range optimization
4. Modern C++ features
5. Auto type deduction"""}
}

class CodeGenerationAPI:
    """Mock API для генерации кода"""
    
    def __init__(self, api_key: str = ""):
        logger.info(f"Initializing Mock CodeGenerationAPI")
        # Mock API не требует ключа
        pass
    
    async def generate_code_async(self, session, prompt: str, model: str, language: str, **kwargs) -> ModelResponse:
        logger.info(f"Generating code for language: {language}, model: {model}")
        logger.debug(f"Additional parameters: {kwargs}")
        
        try:
            if language.lower() not in MOCK_RESPONSES:
                logger.error(f"Language {language} not found in mock responses")
                raise KeyError(f"Language {language} not supported")
                
            if model.lower() not in MOCK_RESPONSES[language.lower()]:
                logger.error(f"Model {model} not found for language {language}")
                raise KeyError(f"Model {model} not supported for {language}")
            
            response_text = MOCK_RESPONSES[language.lower()][model.lower()]
            logger.debug("Successfully retrieved mock response")
            
            return ModelResponse(
                generated_text=response_text,
                raw_response={},
                status=True
            )
        except KeyError as e:
            logger.error(f"KeyError occurred: {str(e)}")
            return ModelResponse(
                generated_text="",
                raw_response={},
                status=False,
                error=f"No mock response for language: {language} and model: {model}"
            )
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}", exc_info=True)
            return ModelResponse(
                generated_text="",
                raw_response={},
                status=False,
                error=f"Error generating code: {str(e)}"
            )