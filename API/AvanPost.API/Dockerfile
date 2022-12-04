FROM mcr.microsoft.com/dotnet/aspnet:6.0 AS base
WORKDIR /app
EXPOSE 80
EXPOSE 443
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        libc6 \
        libgcc1 \
        libgssapi-krb5-2 \
        libssl1.1 \
        libstdc++6 \
        zlib1g \
        gss-ntlmssp \
        jq \
# Clean
    && rm -rf /tmp/* \
        /usr/share/man/?? \
        /usr/share/man/??_* \
        /var/lib/apt-get/lists/* \
        /var/lib/apt/lists/*

FROM mcr.microsoft.com/dotnet/sdk:6.0 AS build
WORKDIR /src
COPY . ./
RUN dotnet restore "API/AvanPost.API/AvanPost.API.csproj"
RUN dotnet build "API/AvanPost.API/AvanPost.API.csproj" -c Release -o /app/build

FROM build AS publish
RUN dotnet publish "API/AvanPost.API/AvanPost.API.csproj" -c Release -o /app/publish

FROM base AS final
ENV DOTNET_RUNNING_IN_CONTAINER=true
ENV ASPNETCORE_HTTP_PORT=80
ENV ASPNETCORE_GRPC_PORT=82
ENV ASPNETCORE_DEBUG_PORT=84

WORKDIR /app
COPY --from=publish /app/publish .
ENTRYPOINT ["dotnet", "AvanPost.API.dll"]
