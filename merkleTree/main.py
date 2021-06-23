import hashlib

def sha256(content):
	return hashlib.sha256(content.encode()).hexdigest()

class MerkleNode:
	def __init__(self, Nodehash):
		self.hash = Nodehash
		self.parent = None
		self.leftChild = None 
		self.rightChild = None
		#self.value = value


class MerkleTree:
	def __init__(self, chunks):
		self.leaves = []
		for chunk in chunks:
			self.leaves.append(MerkleNode(sha256(chunk)))
			#self.leaves.append(MerkleNode(sha256(chunk),chunk))
		
		self.root = self.build_merkle_tree(self.leaves)

	def build_merkle_tree(self,leaves):
		totalLeaves = len(leaves)
		if totalLeaves == 1:
			return leaves[0]
		
		newLeaves = []
		i = 0 
		while i < totalLeaves:
			left = leaves[i]
			right = leaves[i+1] if i+1<totalLeaves else left
			
			parent = MerkleNode(sha256(left.hash+right.hash))
			#parent = MerkleNode(sha256(left.hash+right.hash), left.value+right.value)

			left.parent,right.parent = parent,parent
			parent.leftChild = left
			parent.rightChild = right
			
			newLeaves.append(parent)
			i+=2
		
		return self.build_merkle_tree(newLeaves)

	def audit_trail(self,chunk):
		for leaf in self.leaves:
			if chunk == leaf.hash:
				return self.generate_audit_trail(leaf)
		return False

	def generate_audit_trail(self, chunkNode, trail=[]):

		if chunkNode == self.root:
			trail.append((chunkNode.hash,False))
			return trail

		isleft = chunkNode.parent.leftChild == chunkNode
	
		if isleft:
			trail.append((chunkNode.parent.rightChild.hash, not isleft))
		else:
			trail.append((chunkNode.parent.leftChild.hash, not isleft))

		return self.generate_audit_trail(chunkNode.parent,trail)

	def audit_verify(self, chunk_hash, audit_trail):	
		hash_till_now = chunk_hash
		for node in audit_trail[:-1]:
			isleft = node[1]
			if isleft:
				hash_till_now = sha256(node[0]+hash_till_now)
			else:
				hash_till_now = sha256(hash_till_now+node[0])
			
		return hash_till_now == audit_trail[-1][0]


		

merkle = MerkleTree(["rishabh","avijit","rishabh2", "avijit2"])

audit_trail = merkle.audit_trail(sha256("avijit"))

print(merkle.audit_verify(sha256("avijit"),audit_trail))
#print(list(map(lambda node: (node.value,node.hash), merkle.leaves)))

