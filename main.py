import rosbag
from sensor_msgs.msg import PointCloud2

# Define input bag
input_bag = rosbag.Bag('./rosbags/2022-07-28-23-03-47.bag')

# Define the name of the output bag file
output_fname = './rosbags/merged-2022-07-28-23-03-47.bag'

# Define the topic name of the merged LiDAR Data
merged_topic = '/livox/merged'

# Defined the topic name of the raw LiDAR Data
raw_topic = '/livox/lidar'

# Number of segments
num_segm = 3

# Initialize the point cloud counter
count_PtCld = 0

# Define the Accumulated Point Cloud Data Object
accum_PtCld = PointCloud2() 


# Define output bag
with rosbag.Bag(output_fname, 'w') as output_bag:
    
    for topic, msg, t in input_bag.read_messages(topics=[raw_topic]):
        
        # Write Raw LiDAR data to the new bag file
        output_bag.write(raw_topic, msg, t)
        
        # Increment the count
        count_PtCld += 1
        
        # Get the total width of the point clouds
        accum_PtCld.width += msg.width
        
        # Accumulate the point clouds data
        accum_PtCld.data += msg.data
        
        # If the count reaches the maximum number of segments
        if count_PtCld  == num_segm:
            
            # Define Height of the Point Cloud
            accum_PtCld.height = msg.height
            
            # Get the time of sensor data acquisition
            accum_PtCld.header.stamp = msg.header.stamp
            
            # Get the frame ID
            accum_PtCld.header.frame_id = msg.header.frame_id
            
            # Get the field that describes the channels and their layout in the binary data blob.
            accum_PtCld.fields = msg.fields
            
            # Get the bigendian boolean data
            accum_PtCld.is_bigendian = msg.is_bigendian
            
            # Get the length of a point in bytes
            accum_PtCld.point_step = msg.point_step
            
            # Get the length of a row in bytes
            accum_PtCld.row_step = msg.row_step
            
            # True if there are no invalid points
            accum_PtCld.is_dense = msg.is_dense
            
            # Write to the new bag file's merged LiDAR data topic
            output_bag.write(merged_topic, accum_PtCld, t)
            
            # Reset necessary parameters
            accum_PtCld = PointCloud2()
            accum_PtCld.width = 0
            count_PtCld = 0

            
    
            
            
            
            
        
        

        
        
        
        



