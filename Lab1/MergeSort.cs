using System;
using System.Collections.Generic;
using System.IO;

namespace Algorithms_III
{
    public static class MergeSorter
    {
        public static void SplitToFiles(string filename)
        {
            BinaryReader arrayFile = new BinaryReader(File.Open(filename, FileMode.Open));
            BinaryWriter b1File = new BinaryWriter(File.Open("B1.dat", FileMode.OpenOrCreate));
            BinaryWriter b2File = new BinaryWriter(File.Open("B2.dat", FileMode.OpenOrCreate));
            int count = 0;

            while (arrayFile.BaseStream.Position < arrayFile.BaseStream.Length)
            {
                if (count % 2 == 0)
                {
                    int[] series = _detectSeries(arrayFile);
                    foreach (var num in series)
                        b1File.Write(num);
                }
                else
                {
                    int[] series = _detectSeries(arrayFile);
                    foreach (var num in series)
                        b2File.Write(num);
                }

                count++;
            }
            
            arrayFile.Close();
            b1File.Close();
            b2File.Close();
        }
        
        public static void RecombineFiles(string rootFilename)
        {
            BinaryReader baseFile1;
            long currentLength;
            do
            {
                baseFile1 = new BinaryReader(File.Open("B1.dat", FileMode.OpenOrCreate));
                BinaryReader baseFile2 = new BinaryReader(File.Open("B2.dat", FileMode.OpenOrCreate));
                _recombineSeries(baseFile1, baseFile2, "C1.dat", "C2.dat");
                baseFile1.Close();
                baseFile2.Close();
                File.Delete("B1.dat");
                File.Delete("B2.dat");
                
                baseFile1 = new BinaryReader(File.Open("C1.dat", FileMode.OpenOrCreate));
                baseFile2 = new BinaryReader(File.Open("C2.dat", FileMode.OpenOrCreate));
                _recombineSeries(baseFile1, baseFile2, "B1.dat", "B2.dat");
                currentLength = baseFile1.BaseStream.Length;
                baseFile1.Close();
                baseFile2.Close();
                File.Delete("C1.dat");
                File.Delete("C2.dat");
            } while (currentLength < (new FileInfo(rootFilename).Length));
            
        }
        
        private static void _recombineSeries(BinaryReader baseFile1, BinaryReader baseFile2, string resultFile1, string resultFile2)
        {
            BinaryWriter firstResultFile = new BinaryWriter(File.Open(resultFile1, FileMode.OpenOrCreate));
            BinaryWriter secondResultFile = new BinaryWriter(File.Open(resultFile2, FileMode.OpenOrCreate));
            while (baseFile1.BaseStream.Position < baseFile1.BaseStream.Length && baseFile2.BaseStream.Position < baseFile2.BaseStream.Length)
            {
                int firstSequenceLength = _detectSeriesInFile(baseFile1);
                int secondSequenceLength = _detectSeriesInFile(baseFile2);
                _mergeSeriesToFile(baseFile1, baseFile2, firstResultFile, firstSequenceLength, secondSequenceLength);

                firstSequenceLength = _detectSeriesInFile(baseFile1);
                secondSequenceLength = _detectSeriesInFile(baseFile2);
                _mergeSeriesToFile(baseFile1, baseFile2, secondResultFile, firstSequenceLength, secondSequenceLength);
            }
            
            firstResultFile.Close();
            secondResultFile.Close();
        }

        private static void _mergeSeriesToFile(BinaryReader firstFile, BinaryReader secondFile, BinaryWriter resultFile,
            int firstLength, int secondLength)
        {
            int i = 1;
            int j = 1;
            if (firstLength != 0 && secondLength != 0)
            {
                int num1 = firstFile.ReadInt32();
                int num2 = secondFile.ReadInt32();
                while (i <= firstLength && j <= secondLength)
                {
                    if (num1 == -1)
                        num1 = firstFile.ReadInt32();
                    if (num2 == -1)
                        num2 = secondFile.ReadInt32();

                    if (num1 <= num2)
                    {
                        resultFile.Write(num1);
                        num1 = -1;
                        i++;
                    }
                    else
                    {
                        resultFile.Write(num2);
                        num2 = -1;
                        j++;
                    }
                    
                    while (i <= firstLength)
                    {
                        resultFile.Write(firstFile.ReadInt32());
                        i++;
                    }
                    while (j <= secondLength)
                    {
                        resultFile.Write(secondFile.ReadInt32());
                        j++;
                    }
                }
            }
        }
        
        
        private static int _detectSeriesInFile(BinaryReader file)
        {
            int sequenceLength = 0;
            while (file.BaseStream.Position < file.BaseStream.Length)
            {
                int prevNum;
                int nextNum;
                try
                {
                    prevNum = file.ReadInt32();
                    nextNum = file.ReadInt32();
                }
                catch (Exception e)
                {
                    file.BaseStream.Seek(-4 * sequenceLength, SeekOrigin.Current);
                    return sequenceLength;
                }
                
                sequenceLength += 1;
                
                if (prevNum <= nextNum)
                {
                    file.BaseStream.Seek(-4, SeekOrigin.Current);
                }
                else
                {
                    file.BaseStream.Seek(-4 * sequenceLength, SeekOrigin.Current);
                    return sequenceLength;
                }
            }
            
            return sequenceLength;
        }

        private static int[] _detectSeries(BinaryReader arrayFile)
        {
            bool continueSearching = true;
            List<int> seriesNumbers = new List<int> {arrayFile.ReadInt32()};

            while (continueSearching)
            {
                int nextNum;
                try
                {
                    nextNum = arrayFile.ReadInt32();
                }
                catch (Exception e)
                {
                    return seriesNumbers.ToArray();
                }
                
                if (seriesNumbers[^1] <= nextNum)
                    seriesNumbers.Add(nextNum);
                else
                {
                    arrayFile.BaseStream.Seek(-4, SeekOrigin.Current);
                    continueSearching = false;
                }
            }

            return seriesNumbers.ToArray();
        }
    }
}