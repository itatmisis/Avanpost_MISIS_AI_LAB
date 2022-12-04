using Avanpost.Data.Entities;
using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;

namespace Avanpost.Data.EntitiesConfiguration
{
    internal class ImagesConfiguration : IEntityTypeConfiguration<Images>
    {
        public void Configure(EntityTypeBuilder<Images> builder)
        {
            builder
                .ToTable("images");

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
                .Property(x => x.Path)
                .HasColumnName("path")
                .HasColumnType("text");

            builder
                .Property(x => x.DataClassId)
                .HasColumnName("class_id")
                .HasColumnType("integer");

            builder
                .HasOne(x => x.DataClass)
                .WithMany(x => x.Images)
                .HasForeignKey(x => x.DataClassId);

        }
    }
}
