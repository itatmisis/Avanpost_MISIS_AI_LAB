namespace Avanpost.Data.Entities
{
    public class ModelClass
    {
        public int Id { get; set; }
        public int ModelId { get; set; }
        public int ModelClassId { get; set; }
        public int DataClassId { get; set; }

        public virtual Model Model { get; set; }
        public virtual DataClass DataClass { get; set; }
    }
}
