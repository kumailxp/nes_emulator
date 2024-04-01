#pragma optimize(push, off)
int x = 50;
void a () { 
    asm("LDA _x");
    asm("LDY _x");
    asm("LDX _x");
    asm("LDA #05");
    asm("LDY #15");
    asm("LDX #20");
}
#pragma optimize(pop)