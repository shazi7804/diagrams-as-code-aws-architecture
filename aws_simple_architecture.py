from diagrams import Diagram, Cluster, Edge
from diagrams.aws.compute import EC2
from diagrams.aws.database import Aurora, DDB
from diagrams.aws.network import VPC, CF, ELB, InternetGateway, NATGateway
from diagrams.aws.storage import S3

with Diagram("AWS Simple Architecture", show=False, outformat="png"):
    cf = CF("CloudFront")

    with Cluster("VPC"):
        with Cluster("Private Subnet"):

            with Cluster("App"):
                servers_group = [EC2("app1"), EC2("app2"), EC2("app3")]

            with Cluster("Aurora Cluster"):
                aurora_writer = Aurora("Writer")
                aurora_writer - Aurora("Reader")

        with Cluster("Public Subnet"):

            elb = ELB("ALB")
            igw = InternetGateway("IGW")

            bastion = EC2("Bastion") >> Edge(label="login") >> servers_group[0]

    cf >> igw >> elb >> servers_group
    servers_group[0] >> aurora_writer
