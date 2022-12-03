using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Avanpost.Data.Entities
{
    public class Model
    {
        public int Id { get; set; }
        public string Name { get; set; }
        public string Path { get; set; }
        public int ParentId { get; set; }
        public virtual Model? Parent { get; set; }

        public ICollection<ModelClass> ModelClasses { get; set; }

        public Model()
        {
            ModelClasses = new List<ModelClass>();
        }
    }
}
