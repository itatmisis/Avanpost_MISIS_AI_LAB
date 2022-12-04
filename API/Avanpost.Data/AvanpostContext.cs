using Avanpost.Data.Entities;
using Avanpost.Data.EntitiesConfiguration;
using Microsoft.EntityFrameworkCore;

namespace Avanpost.Data
{
    public class AvanpostContext: DbContext
    {
        public AvanpostContext(DbContextOptions<AvanpostContext> options)
            :base(options)
        {

        }

        public DbSet<DataClass> DataClasses { get; set; }
        public DbSet<ModelClass> ModelClasses { get; set; }
        public DbSet<Model> Models { get; set; }
        public DbSet<Images> Images { get; set; }
        public DbSet<Predict> Predicts { get; set; }
        public DbSet<Train> Trains { get; set; }

        protected override void OnModelCreating(ModelBuilder builder)
        {
            base.OnModelCreating(builder);

            builder.ApplyConfiguration(new DataClassConfiguration());
            builder.ApplyConfiguration(new ModelConfiguration());
            builder.ApplyConfiguration(new ModelClassConfiguration());
            builder.ApplyConfiguration(new ImagesConfiguration());
            builder.ApplyConfiguration(new PredictConfiguration());
            builder.ApplyConfiguration(new TrainConfiguration());
        }


    }
}
