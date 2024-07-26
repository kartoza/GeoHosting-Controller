import React, {useEffect, useRef, useState} from 'react';
import {
  Box,
  Button,
  ChakraProvider,
  Container,
  Flex,
  Heading,
  Image,
  List,
  ListItem,
  Modal,
  ModalBody,
  ModalCloseButton,
  ModalContent,
  ModalHeader,
  ModalOverlay,
  SimpleGrid,
  Spinner,
  Tab,
  TabList,
  TabPanel,
  TabPanels,
  Tabs,
  Text,
  useDisclosure,
  Wrap,
  WrapItem
} from '@chakra-ui/react';
import Navbar from '../../components/Navbar/Navbar';
import ProductCard from "../../components/ProductCard/ProductCard";
import GeonodeIcon from '../../assets/images/GeoNode.svg';
import customTheme from "../../theme/theme";
import {AppDispatch, RootState} from "../../redux/store";
import {useDispatch, useSelector} from "react-redux";
import {fetchProducts, Product} from "../../redux/reducers/productsSlice";
import {CheckIcon} from "@chakra-ui/icons";

const HomePage: React.FC = () => {
  const dispatch: AppDispatch = useDispatch();
  const { products, loading, error } = useSelector((state: RootState) => state.products);
  const [selectedProduct, setSelectedProduct] = useState<Product | null>(null);
  const detailsRef = useRef<HTMLDivElement>(null);
  const { isOpen, onOpen, onClose } = useDisclosure();
  const [popupImage, setPopupImage] = useState<string | null>(null);

  useEffect(() => {
    dispatch(fetchProducts());
  }, [dispatch]);

  const handleProductClick = (product) => {
    setSelectedProduct(product);
     setTimeout(() => {
      detailsRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, 100);
  };

  const handleImageHover = (image) => {
    setPopupImage(image);
    onOpen();
  };

  return (
    <ChakraProvider theme={customTheme}>
      <Flex direction="column" minHeight="100vh">
        <Box flex="1">
          <Navbar />
            <Box
              position="absolute"
              left="0"
              top="0"
              width={{ base: '20vw', md: '14vw', xl: '10vw' }}
              height={{ base: '100vh', md: '100vh', xl: '100%' }}
              background="url('/static/images/right.svg')"
              backgroundSize="cover"
              backgroundRepeat="repeat-y"
              backgroundAttachment="scroll, local;"
              zIndex="-1"
            />
            <Box
              position="absolute"
              right="0"
              top="0"
              width={{ base: '20vw', md: '14vw', xl: '10vw' }}
              height={{ base: '100vh', md: '100vh', xl: '100%' }}
              background="url('/static/images/left.svg')"
              backgroundSize="cover"
              backgroundRepeat="repeat-y"
              backgroundAttachment="scroll, local;"
              zIndex="-1"
            />
            <Container maxW='container.xl' textAlign="center" mt="80px" mb="80px" bg="transparent">
              <Heading as="h1" fontSize={{ base: '5xl', md: '6xl', xl: '7xl' }} fontWeight="thin" color="blue.500" mt="20px">
                GeoSpatialHosting
              </Heading>
              <Text fontSize="lg" marginTop="20px">
                YOUR ONLINE GEOSPATIAL WORKSPACE
              </Text>
              <Text color="gray.700" fontSize={{ base: '2xl', md: '3xl', xl: '4xl' }} marginTop="30px" fontWeight="bold" paddingLeft={50} paddingRight={50}>
                Welcome to a better GIS platform where privacy and freedom come first.
              </Text>
              <Wrap spacing="30px" marginTop="50px" justify="center">
                {loading && <Spinner size='xl' />}
                {error && <Text color="red.500">{error}</Text>}
                {products.map((product) => (
                  <WrapItem key={product.id}>
                    <ProductCard
                      image={product.image ? product.image : GeonodeIcon}
                      title={product.name}
                      description={product.description}
                      comingSoon={product.available}
                      onClick={() => handleProductClick(product)}
                      selected={selectedProduct ? (selectedProduct.id == product.id) : false}
                    />
                  </WrapItem>
                ))}
              </Wrap>
            </Container>
            {selectedProduct && (
              <Container maxW='container.xl' textAlign="center" mt="80px" mb="80px">
                <Box ref={detailsRef} bg="white" p="4" mt="10">
                  <Tabs>
                    <TabList>
                      <Tab>
                        <Image
                          src={selectedProduct.image ? selectedProduct.image : GeonodeIcon}
                          alt={selectedProduct.name}
                          boxSize="30px"
                          mr="2"
                        />
                        Overview</Tab>
                      <Tab>Pricing</Tab>
                    </TabList>
                    <TabPanels>
                      <TabPanel>
                        <SimpleGrid columns={{ base: 1, md: 2, lg: 2 }} spacingX='40px' spacingY={{ base: 10, md: 10, lg: 0 }} backgroundColor={'blue.500'} color={'white'} borderRadius={10} padding={10}>
                          <Box>
                            <Heading as="h3" size="lg" textAlign={'right'}> {selectedProduct.name} Overview</Heading>
                            <Text mt={5} textAlign={"right"} fontSize={20}>
                              GeoNode is a Spatial Data Infrastructure hub with tools for uploading,
                              describing & cataloguing, viewing and sharing your spatial datasets.
                            </Text>
                          </Box>
                          <Box>
                            <Image
                              src={'/static/images/Product_Images/GeoNode/main.png'}
                              alt={'background-overview'}
                              onClick={() => handleImageHover('/static/images/Product_Images/GeoNode/main.png')}
                              style={{
                                'cursor': 'pointer'
                              }}
                            />
                          </Box>
                          <Box>

                          </Box>
                        </SimpleGrid>
                      </TabPanel>
                      <TabPanel>
                        <Heading as="h3" size="lg">{selectedProduct.name} Pricing</Heading>
                        <SimpleGrid columns={{ base: 1, md: 2, lg: 4 }} spacingX='15px' spacingY={{ base: 10, md: 10, lg: 0 }} mt={10}>
                          <Box height={{ base: 150, md: 200, lg: 400 }} backgroundColor={'gray.200'} borderRadius={15} display={'flex'} justifyContent={'center'} alignItems={'center'}>
                            <Image
                              src={selectedProduct.image ? selectedProduct.image : GeonodeIcon}
                              alt={selectedProduct.name}
                              boxSize="60%"
                            />
                          </Box>
                          <Box height={400} backgroundColor={'gray.200'} borderRadius={15} display={'flex'} justifyContent={'flex-start'} alignItems={'center'} flexDirection='column' width={'100%'}>
                            <Box backgroundColor={'blue.500'} textColor={'white'} width={'100%'} borderTopRadius={15} position="sticky" top="0" zIndex="1">
                              <Heading as="h4" size="lg" paddingTop={2} paddingBottom={2} textAlign="center">
                                {selectedProduct.name} Basic
                              </Heading>
                            </Box>
                            <Box mt={4}>
                              <Text fontSize={40} fontWeight={'bold'}>
                                R 131,599
                              </Text>
                              <Text fontSize={20}>
                                /month
                              </Text>
                            </Box>
                            <Box mt={4}>
                              <Button size={'xl'} backgroundColor={'blue.500'} color={'white'} fontWeight={'bold'} paddingTop={5} paddingBottom={5}>Get {selectedProduct.name} Basic</Button>
                            </Box>
                            <Box mt={5} textAlign="center" width="80%" alignItems='center'>
                              <Text fontWeight={'bold'} fontSize={18}>
                                Basic Features
                              </Text>
                              <List spacing={2} mt={2}>
                                <ListItem display="flex" alignItems="center">
                                  <CheckIcon color="green.500" mr={2} /> 60GB storage
                                </ListItem>
                                <ListItem display="flex" alignItems="center">
                                  <CheckIcon color="green.500" mr={2} /> 2 CPUs
                                </ListItem>
                                <ListItem display="flex" alignItems="center">
                                  <CheckIcon color="green.500" mr={2} /> 8GB memory
                                </ListItem>
                              </List>
                            </Box>
                          </Box>
                          <Box height={400} backgroundColor={'gray.200'} borderRadius={15} display={'flex'} justifyContent={'flex-start'} alignItems={'center'} flexDirection='column' width={'100%'}>
                            <Box backgroundColor={'blue.500'} textColor={'white'} width={'100%'} borderTopRadius={15} position="sticky" top="0" zIndex="1">
                              <Heading as="h4" size="lg" paddingTop={2} paddingBottom={2} textAlign="center">
                                {selectedProduct.name} Basic
                              </Heading>
                            </Box>
                            <Box mt={4}>
                              <Text fontSize={40} fontWeight={'bold'}>
                                R 164,874
                              </Text>
                              <Text fontSize={20}>
                                /month
                              </Text>
                            </Box>
                            <Box mt={4}>
                              <Button size={'xl'} backgroundColor={'blue.500'} color={'white'} fontWeight={'bold'} paddingTop={5} paddingBottom={5}>Get {selectedProduct.name} Advanced</Button>
                            </Box>
                            <Box mt={5} textAlign="center" width="80%" alignItems='center'>
                              <Text fontWeight={'bold'} fontSize={18}>
                                Basic Advanced
                              </Text>
                              <List spacing={2} mt={2}>
                                <ListItem display="flex" alignItems="center">
                                  <CheckIcon color="green.500" mr={2} /> 120GB storage
                                </ListItem>
                                <ListItem display="flex" alignItems="center">
                                  <CheckIcon color="green.500" mr={2} /> 4 CPUs
                                </ListItem>
                                <ListItem display="flex" alignItems="center">
                                  <CheckIcon color="green.500" mr={2} /> 16GB memory
                                </ListItem>
                              </List>
                            </Box>
                          </Box>
                          <Box height={400} backgroundColor={'gray.200'} borderRadius={15} display={'flex'} justifyContent={'flex-start'} alignItems={'center'} flexDirection='column' width={'100%'}>
                            <Box backgroundColor={'yellow.400'} textColor={'white'} width={'100%'} borderTopRadius={15} position="sticky" top="0" zIndex="1">
                              <Heading as="h4" size="lg" paddingTop={2} paddingBottom={2} textAlign="center">
                                {selectedProduct.name} Gold
                              </Heading>
                            </Box>
                            <Box mt={4}>
                              <Text fontSize={40} fontWeight={'bold'}>
                                R 181,190
                              </Text>
                              <Text fontSize={20}>
                                /month
                              </Text>
                            </Box>
                            <Box mt={4}>
                              <Button size={'xl'} backgroundColor={'yellow.400'} color={'white'} fontWeight={'bold'} paddingTop={5} paddingBottom={5}>Get {selectedProduct.name} Gold</Button>
                            </Box>
                            <Box mt={5} textAlign="center" width="80%" alignItems='center'>
                              <Text fontWeight={'bold'} fontSize={18}>
                                Gold Features
                              </Text>
                              <List spacing={2} mt={2}>
                                <ListItem display="flex" alignItems="center">
                                  <CheckIcon color="green.500" mr={2} /> 500GB storage
                                </ListItem>
                                <ListItem display="flex" alignItems="center">
                                  <CheckIcon color="green.500" mr={2} /> 4 CPUs
                                </ListItem>
                                <ListItem display="flex" alignItems="center">
                                  <CheckIcon color="green.500" mr={2} /> 32GB memory
                                </ListItem>
                              </List>
                            </Box>
                          </Box>
                        </SimpleGrid>
                      </TabPanel>
                    </TabPanels>
                  </Tabs>
                </Box>
              </Container>
            )}
          </Box>
          <Box
            width="100%"
            backgroundColor="blue.500"
            py="4"
            textAlign="center"
          >
            <Text color="white">Powered by Kartoza</Text>
          </Box>
        </Flex>
        <Modal isOpen={isOpen} onClose={onClose} size={'full'}>
          <ModalOverlay />
          <ModalContent>
            <ModalHeader></ModalHeader>
            <ModalCloseButton />
            <ModalBody>
              <Image src={popupImage ? popupImage : ''} alt="Product Image" width={'100%'}/>
            </ModalBody>
          </ModalContent>
        </Modal>
    </ChakraProvider>
  );
};

export default HomePage;
