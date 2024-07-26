class ReceiverProcess:
    """ Represent the receiver process in the application layer  """
    __buffer = list()

    @staticmethod
    def deliver_data(data):
        """ deliver data from the transport layer RDT receiver to the application layer
        :param data: a character received by the RDT RDT receiver
        :return: no return value
        """
        ReceiverProcess.__buffer.append(data)
        return

    @staticmethod
    def get_buffer():
        """ To get the message the process received over the network
        :return:  a python list of characters represent the incoming message
        """
        return ReceiverProcess.__buffer


class RDTReceiver:
    """" Implement the Reliable Data Transfer Protocol V2.2 Receiver Side """

    def __init__(self):
        self.sequence = '0'

    @staticmethod
    def is_corrupted(packet):
        """ Check if the received packet from sender is corrupted or not
            :param packet: a python dictionary represent a packet received from the sender
            :return: True -> if the reply is corrupted | False ->  if the reply is NOT corrupted
        """
        # TODO provide your own implementation
        if packet['checksum']==ord(packet['data']):
            return False
        else:
            return True

    @staticmethod
    def is_expected_seq(rcv_pkt, exp_seq):
        """ Check if the received reply from receiver has the expected sequence number
         :param rcv_pkt: a python dictionary represent a packet received by the receiver
         :param exp_seq: the receiver expected sequence number '0' or '1' represented as a character
         :return: True -> if ack in the reply match the   expected sequence number otherwise False
        """
        # TODO provide your own implementation
        if rcv_pkt['sequence_number']==exp_seq:
            return True
        else:
            return False


    @staticmethod
    def make_reply_pkt(seq, checksum):
        """ Create a reply (feedback) packet with to acknowledge the received packet
        :param seq: the sequence number '0' or '1' to be acknowledged
        :param checksum: the checksum of the ack the receiver will send to the sender
        :return:  a python dictionary represent a reply (acknowledgement)  packet
        """
        reply_pck = {
            'ack': seq,
            'checksum': checksum
        }
        return reply_pck

    def rdt_rcv(self, rcv_pkt):
        """  Implement the RDT v2.2 for the receiver
        :param rcv_pkt: a packet delivered by the network layer 'udt_send()' to the receiver
        :return: the reply packet
        """

        # TODO provide your own implementation

        # deliver the data to the process in the application layer

        if self.is_corrupted(rcv_pkt) or not self.is_expected_seq(rcv_pkt, self.sequence):#if the received packet is corrupt or with the opp(wrong) seq no
            if(RDTReceiver.is_corrupted(rcv_pkt)):
             print ("corruption occurred: ",rcv_pkt)
            else:
                print('incorrect seq no')
            if (self.sequence =='0'):#if the exp seq no was 0 but i got a 1
                reply_pkt= RDTReceiver.make_reply_pkt('1',ord('1'))#send an ack with seq no 1
            else:
                reply_pkt = RDTReceiver.make_reply_pkt('0',ord('0'))
            print('receiver expecting seq no: '+self.sequence)
        else:#if the received packet is not corrupt and with the correct seq no
            reply_pkt= RDTReceiver.make_reply_pkt(self.sequence,ord(self.sequence))#send an ack with the seq no
            ReceiverProcess.deliver_data(rcv_pkt['data'])#extracts the data
            if(self.sequence == '1'):#moves to the next state
             print('receiver expecting seq no: 1')
             self.sequence = '0'
            else:
              print('receiver expecting seq no: 0')
              self.sequence = '1'
        print("receiver reply with: ",reply_pkt)
        return reply_pkt
    
    