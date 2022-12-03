using Avanpost.Data.Entities;
using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;

namespace Avanpost.Data.EntitiesConfiguration
{
    internal class ModelConfiguration : IEntityTypeConfiguration<Model>
    {
        public void Configure(EntityTypeBuilder<Model> builder)
        {
            builder
                .ToTable("models");

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
                .Property(x => x.ParentId)
                .HasColumnName("parent_id")
                .HasColumnType("integer");

            builder
                .Property(x => x.Name)
                .HasColumnName("name")
                .HasColumnType("text")
                .IsRequired(false);

            builder
                .Property(x => x.Path)
                .HasColumnName("path")
                .HasColumnName("text")
                .IsRequired();
        }
    }
}
