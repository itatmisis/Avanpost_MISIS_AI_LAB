using Avanpost.Data.Entities;
using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;

namespace Avanpost.Data.EntitiesConfiguration
{
    internal class DataClassConfiguration : IEntityTypeConfiguration<DataClass>
    {
        public void Configure(EntityTypeBuilder<DataClass> builder)
        {

            builder
                .ToTable("data_class");

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
                .Property(x => x.Name)
                .HasColumnName("name")
                .HasColumnType("text")
                .IsRequired();

            builder
                .Property(x => x.SamplesNumber)
                .HasColumnName("samples_number")
                .HasColumnType("integer")
                .IsRequired();

        }
    }
}
