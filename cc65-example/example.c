#include <stdio.h>
#include <stdlib.h>

int main()
{
	printf("Hello world!\n");
	// sim65 C applications can use stdio.h standard I/O functions,
	// take keyboard input, read/write files, etc.
	// return the desired error code from main, but note that only the low byte is used.
	return 0;
	// stdlib.h exit may also be used to return immediately with error code
	// exit(0);
}
