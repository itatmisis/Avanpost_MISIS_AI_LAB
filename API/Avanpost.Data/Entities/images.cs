namespace Avanpost.Data.Entities
{
    public class Images
    {
        public int Id { get; set; }
        public string Path { get; set; }
        public int DataClassId { get; set; }
        public virtual DataClass DataClass { get; set; }
    }
}
