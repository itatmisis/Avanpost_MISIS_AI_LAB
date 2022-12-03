#See https://aka.ms/containerfastmode to understand how Visual Studio uses this Dockerfile to build your images for faster debugging.

FROM mcr.microsoft.com/dotnet/aspnet:5.0 AS base
WORKDIR /app
EXPOSE 80
EXPOSE 443

FROM mcr.microsoft.com/dotnet/sdk:5.0 AS build
WORKDIR /src
COPY ["API/AvanPost.API/AvanPost.API.csproj", "AvanPost.API/"]
COPY ["API/Avanpost.Data/Avanpost.Data.csproj", "Avanpost.Data/"]
RUN dotnet restore "AvanPost.API/AvanPost.API.csproj"
COPY . .
WORKDIR "/src/AvanPost.API"
RUN dotnet build "AvanPost.API.csproj" -c Release -o /app/build

FROM build AS publish
RUN dotnet publish "AvanPost.API.csproj" -c Release -o /app/publish

FROM base AS final
WORKDIR /app
COPY --from=publish /app/publish .
ENTRYPOINT ["dotnet", "AvanPost.API.dll"]