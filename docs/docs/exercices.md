# Some exercises

!!! exercise "Clouds"

    What is the color of the sky ?

    - [ ] Red
    - [ ] Green
    - [x] Blue
    - [ ] Yellow

    !!! solution

        The sky is blue because of Rayleigh scattering.

!!! exercise "Hello World"

    Complete the following program:

    ```c
    #include <stdio.h>

    int main() {
    }
    ```

    ```yml
    tests:
        - name: "Build"
          builds: true
        - name: "Hello World"
          args: []
          stdout: "Hello World!"
    ```