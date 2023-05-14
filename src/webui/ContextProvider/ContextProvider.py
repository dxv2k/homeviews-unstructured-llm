from typing import Dict, Callable, Any, Optional


class ContextProvider:
    ''' 
    # Un-used at this point
    ``` 
    context = ContextProvider.create()
    ``` 

    #### Define some functions that use variables from the context
    ```
    @context.register('x')
    def square_x(x):
        return x ** 2

    @context.register('y')
    def double_y(y):
        return y * 2
    ```

    #### Set the initial values of the variables
    ```
    context.set_vars(x=10, y=20)
    ```

    #### Call the functions and print the results
    ```
    print(square_x())  # Output: 100
    print(double_y())  # Output: 40
    ```

    #### Update the value of a variable and call the function again
    ```
    context.set_vars(x=5)
    print(square_x())  # Output: 25
    ```

    '''
    def __init__(self, initial_values: Optional[Dict[str, Any]] = None) -> None:
        # Initialize the context provider with an optional dictionary of initial values.
        self._vars: Dict[str, Any] = initial_values or {}

    @classmethod
    def create(cls, initial_values: Optional[Dict[str, Any]] = None) -> "ContextProvider":
        # A convenience method to create a new instance of the context provider.
        # This allows creating a context provider with initial values in a single line of code.
        return cls(initial_values)

    def register(self, name: str) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
        # A decorator that registers a function with the context provider and binds it to a variable name.
        # The decorator returns a wrapper function that calls the original function with the value of the variable.
        def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
            def wrapper(*args: Any, **kwargs: Any) -> Any:
                try:
                    value = self._vars[name]
                except KeyError:
                    raise ValueError(f"Variable '{name}' is not defined")
                return func(value, *args, **kwargs)
            return wrapper
        return decorator

    def set_vars(self, **kwargs: Any) -> None:
        # Set the values of multiple variables in the context provider.
        self._vars.update(kwargs)

    def get(self, name: str) -> Any:
        # Get the value of a variable from the context provider.
        # Raises a ValueError if the variable is not defined.
        try:
            return self._vars[name]
        except KeyError:
            raise ValueError(f"Variable '{name}' is not defined")

    def reset(self, initial_values: Optional[Dict[str, Any]] = None) -> None:
        # Reset the context provider to its initial state.
        # Optionally, set new initial values for the variables.
        self._vars = initial_values or {}
