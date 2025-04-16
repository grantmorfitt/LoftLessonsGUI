import grpc
import StateStore_pb2_grpc as pb2_grpc
import StateStore_pb2 as pb2
import time

class Client(object):
    """
    Client for gRPC functionality
    """

    def __init__(self):
        self.host = '192.168.168.10'
        self.server_port = 5011

        # instantiate a channel
        self.channel = grpc.insecure_channel(
            '{}:{}'.format(self.host, self.server_port))

        # bind the client and the server
        self.stub = pb2_grpc.StateStoreStub(self.channel)

    # def get_url(self, message):
    #     """
    #     Client function to call the rpc for GetServerResponse
    #     """
    #     message = pb2.ReadStates(message=message)
    #     print(f'{message}')
    #     return self.stub.GetServerResponse(message)

dictOptions = {"0" : "double2_value",
               "1" : "blah blah value"
               
               }
                   
if __name__ == '__main__':
    client = Client()
    #result = client.get_url(message="Hello Server you there?")
    
##    randomThing = client.stub.ReadStates(lat_req)
##    print(f'{randomThing}')
##    
##    myList = randomThing.values
##    
##    print("There are {} values in the response".format(len(myList)))
##    
##    for i in myList:
##        #print(i.WhichOneof("value") )
##        current_value_type = i.WhichOneof("value")
##        if current_value_type == "boolean_value":
##            print("We receive a boolean_value. {}".format(i.boolean_value))
##        elif current_value_type == "int32_value":
##            print("We receive a int32_value. {}".format(i.int32_value))
##        elif current_value_type == "double2_value":
##            print("We receive a double2_value. {} - {}".format(i.double2_value.value_0, i.double2_value.value_1))
##        elif current_value_type == "double3_value":
##            print("We receive a double2_value. {} - {}".format(i.double3_value.value_0, i.double3_value.value_1,  i.double3_value.value_2))         
##        elif current_value_type == "double4_value":
##            print("We receive a double4_value. {} - {} - {} - {}".format(i.double4_value.value_0, i.double4_value.value_1,  i.double4_value.value_2, i.double4_value.value_3))            
##        elif current_value_type == "double5_value":
##            print("We receive a double5_value. {} - {} - {} - {} - {}".format(i.double5_value.value_0, i.double5_value.value_1,  i.double5_value.value_2, i.double5_value_3, i.double5_value_4))
##            
    # Subscribe to stream
    # Old states ID: 2496586604, 1666704728, 3917330120, 2457184866
    # This is the request for subscribing to the state IDs
    sub_request = pb2.SubscribeStatesRequest(state_ids=[2142867155,1847367549,1501357761,518160218,4054750327,1049691088,3771464240,1901182077,1162389881,4021288050,2716830861,3063191758,2400822283,1909389254,2496586604,1666704728,1931956084,2074986628,4056189073,855504072,513685691,1553784294,1095517217,1796138214,4247030081,3066527403,3606674210,2176349777,1440247258,3845500168,2936800735,4028988999,1088936463,289709335,2009533588,1949388887,855358880,4202393567,1059500221,2876656444,3599019297,614270119,3590140009,482521778,3917330120,1450782446,3871827618],
                                      notify_empty_change_sets = True,
                                      notify_unchanged = True,
                                      minimum_notification_interval_ms = 300)
    
    # Then we subscribe to the stream
    subcribe_response = client.stub.SubscribeStates(sub_request)
    oldtime = time.time();
    
    for reply in subcribe_response:
        newtime = time.time()
        #print("I'm printing: " + str(reply))
        value_array = reply.values
        #Each return_value should be StateValue
        #And each StateValue should have state ID and an union of value
        for return_value in value_array:
            current_value_type = return_value.WhichOneof("value")
            if current_value_type == "boolean_value":
                print("We receive a boolean_value. {}".format(return_value.boolean_value))
            elif current_value_type == "int32_value":
                print("We receive a int32_value. {}".format(return_value.int32_value))
            elif current_value_type == "double2_value":
                print("We receive a double2_value. {} - {}".format(return_value.double2_value.value_0, return_value.double2_value.value_1))
            elif current_value_type == "double3_value":
                print("We receive a double2_value. {} - {}".format(return_value.double3_value.value_0, return_value.double3_value.value_1,  return_value.double3_value.value_2))         
            elif current_value_type == "double4_value":
                print("We receive a double4_value. {} - {} - {} - {}".format(return_value.double4_value.value_0, return_value.double4_value.value_1,  return_value.double4_value.value_2, return_value.double4_value.value_3))            
            elif current_value_type == "double5_value":
                print("We receive a double5_value. {} - {} - {} - {} - {}".format(return_value.double5_value.value_0, return_value.double5_value.value_1,  return_value.double5_value.value_2, return_value.double5_value_3, return_value.double5_value_4))
        
        print("time elasped: " + str(newtime - oldtime))
        
        oldtime = newtime
