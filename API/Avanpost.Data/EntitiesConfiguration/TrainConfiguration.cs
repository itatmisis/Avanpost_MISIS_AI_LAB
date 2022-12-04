using Avanpost.Data.Entities;
using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;

namespace Avanpost.Data.EntitiesConfiguration
{
    public class TrainConfiguration : IEntityTypeConfiguration<Train>
    {
        public void Configure(EntityTypeBuilder<Train> builder)
        {

            builder
                .ToTable("train");

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
                .Property(x => x.Percent)
                .HasColumnName("percent")
                .HasColumnType("float");

            builder
                .Property(x => x.Status)
                .HasColumnName("status")
                .HasColumnType("int");

            builder
                .Property(x => x.Dataset)
                .HasColumnName("dataset")
                .HasColumnType("text");
        }
    }
}
