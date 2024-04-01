#pragma optimize(push, off)
int x = 50;
void a () { 
    asm("CLC");
    asm("LDA #8");
    asm("STA $0019"); // 5
    asm("LDY #2");
    asm("LDX 23,Y");
    asm("LDA #05"); // 5
    asm("ADC #5");  // 10
    asm("SBC #3");  // 7
    asm("ADC #4");  // 11
    asm("ADC $8004"); 
    asm("LDA _x");
    asm("LDY _x");
    asm("LDX _x");
    asm("LDA #05");
    asm("LDY #15");
    asm("LDX #20");
}
#pragma optimize(pop)