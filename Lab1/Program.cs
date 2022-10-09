namespace Algorithms_III
{
    class Program
    {
        static void Main(string[] args)
        {
            MergeSorter.SplitToFiles("testArrayData.dat");
            MergeSorter.RecombineFiles("testArrayData.dat");
            
            ModifiedMergeSorter.MakeChunks("arrayFile.dat", 16);
            ModifiedMergeSorter.SortChunks(16);
            ModifiedMergeSorter.MergeChunks();
        }
    }
}
