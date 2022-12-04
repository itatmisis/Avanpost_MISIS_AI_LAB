using Avanpost.Data.Entities;
using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;

namespace Avanpost.Data.EntitiesConfiguration
{
    internal class PredictConfiguration : IEntityTypeConfiguration<Predict>
    {
        public void Configure(EntityTypeBuilder<Predict> builder)
        {
            builder
                .ToTable("predict");


            builder
              .HasKey(x => x.Id);

            builder
                .Property(x => x.Id)
                 .ValueGeneratedOnAdd();

            builder
                .Property(x => x.Id)
                .HasColumnName("id")
                .HasColumnType("integer");

            builder
                .Property(x => x.ClassName)
                .HasColumnName("class_name")
                .HasColumnType("text");

            builder
                .Property(x => x.Key)
                .HasColumnName("key")
                .HasColumnType("string");

            builder
                .Property(x => x.Percent)
                .HasColumnName("percent")
                .HasColumnType("float");


        }
    }
}
