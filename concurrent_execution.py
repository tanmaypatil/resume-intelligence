from concurrent.futures import ProcessPoolExecutor, as_completed
import time

# Define two tasks that will run concurrently
def task_1():
    print("Task 1 is starting...")
    time.sleep(5)  # Simulate work with a 2-second delay
    print("Task 1 is complete.")
    return "Result from Task 1"

def task_2():
    print("Task 2 is starting...")
    time.sleep(2)  # Simulate work with a 3-second delay
    print("Task 2 is complete.")
    return "Result from Task 2"

# Use ProcessPoolExecutor to run the tasks concurrently
def run_tasks():
    with ProcessPoolExecutor() as executor:
        future_to_task = {
        executor.submit(task_1): "Task 1",
        executor.submit(task_2): "Task 2",
    }
        # Submit the tasks to the executor
        future_task1 = executor.submit(task_1)
        future_task2 = executor.submit(task_2)

        # Wait for both tasks to complete before returning the results
        results = []
        for future in as_completed(future_to_task):
            task_name = future_to_task[future] 
            result = future.result()  # Retrieve the result of each task
            print(f"{task_name}: {result}")
            results.append(result)
        
        return results

# Execute and print the results
if __name__ == "__main__":
    results = run_tasks()
    print(f"All tasks completed. Results: {results}")
