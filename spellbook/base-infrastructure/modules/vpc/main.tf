# modules/vpc/main.tf

resource "aws_vpc" "main" {
  cidr_block           = var.vpc_cidr
  enable_dns_hostnames = true
  enable_dns_support   = true

  tags = merge(
    {
      Name        = "${var.project_name}-vpc"
      Environment = var.environment
    },
    var.tags
  )
}

resource "aws_internet_gateway" "main" {
  vpc_id = aws_vpc.main.id

  tags = merge(
    {
      Name        = "${var.project_name}-igw"
      Environment = var.environment
    },
    var.tags
  )
}

resource "aws_subnet" "public" {
  count             = length(var.public_subnet_cidrs)
  vpc_id            = aws_vpc.main.id
  cidr_block        = var.public_subnet_cidrs[count.index]
  availability_zone = "${var.aws_region}${count.index == 0 ? "a" : "c"}"

  map_public_ip_on_launch = true

  tags = merge(
    {
      Name        = "${var.project_name}-public-subnet-${count.index + 1}"
      Environment = var.environment
    },
    var.tags
  )
}

resource "aws_subnet" "private" {
  count             = length(var.private_subnet_cidrs)
  vpc_id            = aws_vpc.main.id
  cidr_block        = var.private_subnet_cidrs[count.index]
  availability_zone = "${var.aws_region}${count.index == 0 ? "a" : "c"}"

  tags = merge(
    {
      Name        = "${var.project_name}-private-subnet-${count.index + 1}"
      Environment = var.environment
    },
    var.tags
  )
}

resource "aws_eip" "nat" {
  count = length(var.private_subnet_cidrs) > 0 ? 1 : 0
  vpc   = true

  tags = merge(
    {
      Name        = "${var.project_name}-nat-eip"
      Environment = var.environment
    },
    var.tags
  )
}

resource "aws_nat_gateway" "main" {
  count         = length(var.private_subnet_cidrs) > 0 ? 1 : 0
  allocation_id = aws_eip.nat[0].id
  subnet_id     = aws_subnet.public[0].id

  tags = merge(
    {
      Name        = "${var.project_name}-nat"
      Environment = var.environment
    },
    var.tags
  )
}

resource "aws_route_table" "public" {
  vpc_id = aws_vpc.main.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.main.id
  }

  tags = merge(
    {
      Name        = "${var.project_name}-public-rt"
      Environment = var.environment
    },
    var.tags
  )
}

resource "aws_route_table" "private" {
  count  = length(var.private_subnet_cidrs) > 0 ? 1 : 0
  vpc_id = aws_vpc.main.id

  route {
    cidr_block     = "0.0.0.0/0"
    nat_gateway_id = aws_nat_gateway.main[0].id
  }

  tags = merge(
    {
      Name        = "${var.project_name}-private-rt"
      Environment = var.environment
    },
    var.tags
  )
}

resource "aws_route_table_association" "public" {
  count          = length(var.public_subnet_cidrs)
  subnet_id      = aws_subnet.public[count.index].id
  route_table_id = aws_route_table.public.id
}

resource "aws_route_table_association" "private" {
  count          = length(var.private_subnet_cidrs)
  subnet_id      = aws_subnet.private[count.index].id
  route_table_id = aws_route_table.private[0].id
}
