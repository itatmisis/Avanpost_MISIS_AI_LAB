namespace Avanpost.Data.Entities
{
    public class Predict
    {
        public int Id { get; set; }
        public string Key { get; set; }
        public int Status { get; set; }
        public float Percent { get; set; }
        public string ClassName { get; set; }
    }
}
