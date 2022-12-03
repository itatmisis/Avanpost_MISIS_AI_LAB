using System.Collections.Generic;
using System.ComponentModel.DataAnnotations.Schema;

namespace Avanpost.Data.Entities
{
    public class DataClass
    {
        public int Id { get; set; }
        public string Name { get; set; }
        public int SamplesNumber { get; set; }

        public ICollection<ModelClass> ModelClasses { get; set; }

        public ICollection<Images> Images { get; set; }

        public DataClass()
        {
            ModelClasses = new List<ModelClass>();
            Images = new List<Images>();
        }
    }
}
