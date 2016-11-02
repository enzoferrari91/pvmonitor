// Include Emon Library
#include "EmonLib.h" 

// Create three instances
EnergyMonitor ct1, ct2, ct3;

double P_CT1 = 0; double P_CT2 = 0; double P_CT3 = 0; double P_SUM = 0;
double I_CT1 = 0; double I_CT2 = 0; double I_CT3 = 0;

int U_CT1 = 233; int U_CT2 = 233; int U_CT3 = 233;

const double threshold = 0.01; // Threshold for current 10 mA
char c;

void setup()
{
    Serial.begin(9600);

    ct1.current(0, 10); 
    ct2.current(1, 10);
    ct3.current(2, 10);
}

void loop()
{
	I_CT1 = ct1.calcIrms(1480);
	I_CT2 = ct2.calcIrms(1480);
	I_CT3 = ct3.calcIrms(1480);

	// Debugging
	/*
	Serial.print(I_CT1);
	Serial.print("  ");
	Serial.print(I_CT2);
	Serial.print("  ");
	Serial.print(I_CT3);
	*/

    if (Serial.available()>0)
    {	
		while (Serial.available() > 0)
		{
			// Read comma-seperated voltages from Smart-Meter
			c=Serial.read();
		}

		if(I_CT1 < threshold) { I_CT1 = 0; }
		if(I_CT2 < threshold) { I_CT2 = 0; }
		if(I_CT3 < threshold) { I_CT3 = 0; }
		
		P_CT1 = I_CT1 * U_CT1;
		P_CT2 = I_CT2 * U_CT2;
		P_CT3 = I_CT3 * U_CT3;
		
		P_SUM = P_CT1 + P_CT2 + P_CT3;

        Serial.print(P_SUM);
        Serial.print("!"); // Ende-Zeichen
    }
}
