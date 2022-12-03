using Avanpost.Data.Entities;
using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;

namespace Avanpost.Data.EntitiesConfiguration
{
    internal class ModelClassConfiguration : IEntityTypeConfiguration<ModelClass>
    {
        public void Configure(EntityTypeBuilder<ModelClass> builder)
        {
            builder
                .ToTable("model_class");


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
                .Property(x => x.ModelId)
                .HasColumnName("model_id")
                .HasColumnType("integer")
                .IsRequired();

            builder
                .Property(x => x.ModelClassId)
                .HasColumnName("class_id")
                .HasColumnType("integer")
                .IsRequired();

            builder.HasOne(x => x.DataClass)
                .WithMany(x => x.ModelClasses)
                .HasForeignKey(x => x.DataClassId);

            builder.HasOne(x => x.Model)
                .WithMany(x => x.ModelClasses)
                .HasForeignKey(x => x.ModelId);
        }
    }
}
