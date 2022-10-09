using System;
using System.IO;

namespace Algorithms_III
{
    public static class ModifiedMergeSorter
    {
        public static void MakeChunks(string filename, int numberOfChunks)
        {
            int chunkSize = (int) ((new FileInfo(filename)).Length / numberOfChunks);
            BinaryReader br = new BinaryReader(File.Open(filename, FileMode.Open));

            for (int i = 1; i <= numberOfChunks; i++)
            {
                BinaryWriter fs = new BinaryWriter(File.Open($"B{i}.dat", FileMode.OpenOrCreate));
                byte[] buffer = new byte[chunkSize];
                br.Read(buffer, 0, chunkSize);
                fs.Write(buffer);
                fs.Close();
            }
            br.Close();
        }

        public static void SortChunks(int numberOfChunks)
        {
            for (int i = 1; i <= numberOfChunks; i++)
            {
                BinaryReader br = new BinaryReader(File.Open($"B{i}.dat", FileMode.Open));
                int chunkSize = (int)(new FileInfo($"B{i}.dat")).Length;
                int[] buffer = new int[chunkSize / 4];
                
                for (int j = 0; j < buffer.Length; j++)
                    buffer[j] = br.ReadInt32();
                
                br.Close();
                Array.Sort(buffer);
                BinaryWriter bw = new BinaryWriter(File.Open($"C{i}.dat", FileMode.OpenOrCreate));
                
                foreach (var value in buffer)
                    bw.Write(value);

                bw.Write(int.MaxValue);
                bw.Close();
            }
        }

        public static void MergeChunks()
        {
            for (int i = 1; i <= 16; i++)
            {
                FileInfo fileInf = new FileInfo($"B{i}.dat");
                fileInf.Delete();
            }
            
            for (int i = 1; i <= 16; i += 2)
            {
                BinaryReader br1 = new BinaryReader(File.Open($"C{i}.dat", FileMode.Open));
                BinaryReader br2 = new BinaryReader(File.Open($"C{i + 1}.dat", FileMode.Open));
                BinaryWriter resultFile = new BinaryWriter(File.Open($"B{(i + 1) / 2}.dat", FileMode.OpenOrCreate));
                _merge(br1, br2, resultFile);
                resultFile.Close();
                br1.Close();
                br2.Close();
            }
            
            for (int i = 1; i <= 16; i++)
            {
                FileInfo fileInf = new FileInfo($"C{i}.dat");
                fileInf.Delete();
            }
            
            for (int i = 1; i <= 8; i += 2)
            {
                BinaryReader br1 = new BinaryReader(File.Open($"B{i}.dat", FileMode.Open));
                BinaryReader br2 = new BinaryReader(File.Open($"B{i + 1}.dat", FileMode.Open));
                BinaryWriter resultFile = new BinaryWriter(File.Open($"C{(i + 1) / 2}.dat", FileMode.OpenOrCreate));
                _merge(br1, br2, resultFile);
                resultFile.Close();
                br1.Close();
                br2.Close();
            }

            for (int i = 0; i <= 8; i++)
            {
                FileInfo fileInf = new FileInfo($"B{i}.dat");
                fileInf.Delete();
            }
            
            for (int i = 1; i <= 4; i += 2)
            {
                BinaryReader br1 = new BinaryReader(File.Open($"C{i}.dat", FileMode.Open));
                BinaryReader br2 = new BinaryReader(File.Open($"C{i + 1}.dat", FileMode.Open));
                BinaryWriter resultFile = new BinaryWriter(File.Open($"B{(i + 1) / 2}.dat", FileMode.OpenOrCreate));
                _merge(br1, br2, resultFile);
                resultFile.Close();
                br1.Close();
                br2.Close();
            }
            
            for (int i = 0; i <= 4; i++)
            {
                FileInfo fileInf = new FileInfo($"C{i}.dat");
                fileInf.Delete();
            }
            
            for (int i = 1; i <= 2; i += 2)
            {
                BinaryReader br1 = new BinaryReader(File.Open($"B{i}.dat", FileMode.Open));
                BinaryReader br2 = new BinaryReader(File.Open($"B{i + 1}.dat", FileMode.Open));
                BinaryWriter resultFile = new BinaryWriter(File.Open("resultFile.dat", FileMode.OpenOrCreate));
                _merge(br1, br2, resultFile);
                resultFile.Close();
                br1.Close();
                br2.Close();
            }
        }

        private static void _merge(BinaryReader file1, BinaryReader file2, BinaryWriter resultFile)
        {
            bool continueReading = true;
            int num1 = file1.ReadInt32();
            int num2 = file2.ReadInt32();

            while (continueReading)
            {
                if (num1 == -1)
                    num1 = file1.ReadInt32();
                if (num2 == -1)
                    num2 = file2.ReadInt32();

                if (num1 != int.MaxValue && num2 != int.MaxValue)
                {
                    if (num1 <= num2)
                    {
                        resultFile.Write(num1);
                        num1 = -1;
                    }
                    else
                    {
                        resultFile.Write(num2);
                        num2 = -1;
                    }
                }
                else
                {
                    if (num1 != int.MaxValue)
                    {
                        resultFile.Write(num1);
                        num1 = -1;
                    }
                    if (num2 != int.MaxValue)
                    {
                        resultFile.Write(num2);
                        num2 = -1;
                    }
                }

                if (num1 == int.MaxValue && num2 == int.MaxValue)
                    continueReading = false;
            }
            resultFile.Write(int.MaxValue);
        }


        private static byte[] _readBytes(Stream stream, int chunkSize, int startingPont)
        {
            byte[] buffer = new byte[chunkSize];
            using(BinaryReader reader = new BinaryReader(stream))
            {
                reader.BaseStream.Seek(startingPont, SeekOrigin.Begin);
                reader.Read(buffer, 0, chunkSize);
            }

            return buffer;
        }
    }
}