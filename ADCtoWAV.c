#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <stdint.h>

int ADC_to_16bit(int value);
int Bytes_second_cal(int sampleRate, int bitsPerSample, int numberChannel);
int Bytes_sample_channel_cal(int bitsPerSample, int numberChannel);
void little_endian(int value, int bytes, FILE *fptr);

int main(int argc, char *argv[])
{
    if (argc != 4)
    {
        printf("Please enter input file and output file!!!!\n");
        return 1;
    }
    int sizeData = atoi(argv[3]);
    printf("%d",sizeData);

    int byteHeader = 44;
    int fileSize = sizeData + byteHeader;
    int chunkMarker = 16;
    int audioFormat = 1;
    int audioChannel = 1;
    int samplingRate = 10000; // 6400;
    int bitsPerSample = 8; //16;
    int bps = 0; // bytes per second
    int bpsc = 0; // bytes per sample per channel
    uint16_t ADCData;
    int16_t scaledBit;

    FILE* readPtr = fopen(argv[1], "rb");
    if (readPtr == NULL)
    {
        printf("Error Reading File...");
        return 1;
    }
    FILE* output = fopen(argv[2], "wb");
    if (output == NULL)
    {
        printf("Error Creating File...");
        return 1;
    }

    fwrite("RIFF", 1, 4, output);
    little_endian(fileSize, 4, output);
    fwrite("WAVE", 1, 4, output);
    fwrite("fmt ", 1, 4, output);
    little_endian(chunkMarker, 4, output);
    little_endian(audioFormat, 2, output);
    little_endian(audioChannel, 2, output);
    little_endian(samplingRate, 4, output);

    bps = Bytes_second_cal(samplingRate, bitsPerSample, audioChannel); 
    little_endian(bps, 4, output);

    bpsc = Bytes_sample_channel_cal(bitsPerSample, audioChannel);
    little_endian(bpsc, 2, output);

    little_endian(bitsPerSample, 2, output);
    fwrite("data", 1, 4, output);  
    little_endian(sizeData, 4, output);

    uint8_t sample8;
    while (fread(&ADCData, sizeof(uint8_t), 1, readPtr) == 1)
    {
        sample8 = ADCData;
        fputc(sample8, output);
    }

    // while (fread(&ADCData, sizeof(uint16_t), 1, readPtr) == 1)
    // {
    //     scaledBit = ADC_to_16bit(ADCData);
    //     little_endian(scaledBit, 2, output);
    // }

    fclose(readPtr);
    fclose(output);
}

// int ADC_to_16bit(int value)
// {
//     // since ADC range from 0 to 4095, shift it to center of 0
//     value -= 2048;
//     // then scale it from range of -2048 to +2048 into -32768 to +32767
//     value *= 16;
//     return value;
// }

void little_endian(int value, int bytes, FILE *fptr) 
{
    for (int i = 0; i < bytes; i++) {
        fputc((value >> (8 * i)) & 0xFF, fptr);
    }
}

int Bytes_second_cal(int sampleRate, int bitsPerSample, int numberChannel)
{
    return ((sampleRate*bitsPerSample*numberChannel)/8);
}

int Bytes_sample_channel_cal(int bitsPerSample, int numberChannel)
{
    return((bitsPerSample*numberChannel)/8);
}