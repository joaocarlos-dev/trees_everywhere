from decimal import Decimal
from django.test import Client, TestCase
from django.urls import reverse
from trees.models import Tree, PlantedTree
from accounts.models import Account
from django.contrib.auth import get_user_model

User = get_user_model()


class MyTreesTemplateTest(TestCase):
    def setUp(self):
        self.account1 = Account.objects.create(name="Account 1")
        self.account2 = Account.objects.create(name="Account 2")

        self.user1 = User.objects.create_user(
            username="john", password="password123")
        self.user2 = User.objects.create_user(
            username="mary", password="password123")
        self.user3 = User.objects.create_user(
            username="luke", password="password123")

        self.account1.users.set([self.user1, self.user2])
        self.account2.users.set([self.user2, self.user3])

        self.tree1 = Tree.objects.create(
            name="Yellow Ipe", scientific_name="Handroanthus albus")
        self.tree2 = Tree.objects.create(
            name="Brazilwood", scientific_name="Paubrasilia echinata")

        self.planted1 = PlantedTree.objects.create(user=self.user1, tree=self.tree1, age=2, account=self.account1,
                                                   latitude=12.345678, longitude=98.765432)
        self.planted2 = PlantedTree.objects.create(user=self.user2, tree=self.tree2, age=1, account=self.account1,
                                                   latitude=23.456789, longitude=87.654321)
        self.planted3 = PlantedTree.objects.create(user=self.user3, tree=self.tree1, age=3, account=self.account2,
                                                   latitude=34.567890, longitude=76.543210)

    def test_my_trees_template_lists_only_user_trees(self):
        self.client.login(username="john", password="password123")

        response = self.client.get(reverse("my_trees"))

        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(response, "trees/my_trees.html")

        self.assertContains(response, "Yellow Ipe")

        self.assertNotContains(response, "Brazilwood")


class ForbiddenAccessTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username="user1", password="pass")
        self.user2 = User.objects.create_user(
            username="user2", password="pass")

        self.account = Account.objects.create(name="Account1", active=True)
        self.account.users.add(self.user1, self.user2)

        self.tree = Tree.objects.create(
            name="Test Tree", scientific_name="Testus treeus")

        self.planted_tree_user1 = PlantedTree.objects.create(
            user=self.user1,
            tree=self.tree,
            account=self.account,
            age=5,
            latitude=Decimal("10.000000"),
            longitude=Decimal("20.000000")
        )

        self.client = Client()
        self.client.login(username="user2", password="pass")

    def test_access_other_users_trees_forbidden(self):
        url = reverse("planted_tree_detail", kwargs={
                      "pk": self.planted_tree_user1.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)


class TreesInUserAccountsTemplateTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username='user1', password='pass')
        self.user2 = User.objects.create_user(
            username='user2', password='pass')
        self.user3 = User.objects.create_user(
            username='user3', password='pass')

        self.account1 = Account.objects.create(name='Account 1', active=True)
        self.account2 = Account.objects.create(name='Account 2', active=True)

        self.account1.users.add(self.user1, self.user2)
        self.account2.users.add(self.user3)
        self.tree1 = Tree.objects.create(name='Oak', scientific_name='Quercus')
        self.tree2 = Tree.objects.create(name='Pine', scientific_name='Pinus')

        self.planted_tree1 = PlantedTree.objects.create(
            user=self.user1,
            tree=self.tree1,
            account=self.account1,
            age=3,
            latitude=Decimal('10.123456'),
            longitude=Decimal('20.123456')
        )
        self.planted_tree2 = PlantedTree.objects.create(
            user=self.user2,
            tree=self.tree2,
            account=self.account1,
            age=5,
            latitude=Decimal('11.654321'),
            longitude=Decimal('21.654321')
        )

        self.planted_tree3 = PlantedTree.objects.create(
            user=self.user3,
            tree=self.tree1,
            account=self.account2,
            age=2,
            latitude=Decimal('30.123456'),
            longitude=Decimal('40.123456')
        )

        self.client = Client()
        self.client.login(username='user1', password='pass')

    def test_trees_listed_for_user_accounts(self):
        url = reverse('trees_in_accounts')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(response, 'trees/trees_in_accounts.html')

        trees_in_response = response.context['planted_trees']

        self.assertIn(self.planted_tree1, trees_in_response)
        self.assertIn(self.planted_tree2, trees_in_response)

        self.assertNotIn(self.planted_tree3, trees_in_response)


class UserPlantTreeMethodTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="123456")
        self.account = Account.objects.create(name="Test Account")
        self.user.accounts.add(self.account)  # type: ignore
        self.tree = Tree.objects.create(name="Oak", scientific_name="Quercus")

    def test_plant_tree_creates_planted_tree(self):
        location = (Decimal('10.123456'), Decimal('-20.654321'))
        age = 5

        planted_tree = self.user.plant_tree(  # type: ignore
            tree=self.tree,
            location=location,
            account=self.account,
            age=age
        )

        self.assertIsInstance(planted_tree, PlantedTree)
        self.assertEqual(planted_tree.user, self.user)
        self.assertEqual(planted_tree.tree, self.tree)
        self.assertEqual(planted_tree.account, self.account)
        self.assertEqual(planted_tree.latitude, location[0])
        self.assertEqual(planted_tree.longitude, location[1])
        self.assertEqual(planted_tree.age, age)

        self.assertTrue(PlantedTree.objects.filter(
            pk=planted_tree.pk).exists())

    def test_plant_trees_creates_multiple_planted_trees(self):
        plants = [
            (self.tree, (Decimal('10.000001'), Decimal('20.000001'))),
            (self.tree, (Decimal('15.123456'), Decimal('25.654321'))),
        ]

        planted_trees = self.user.plant_trees(  # type: ignore
            plants=plants, account=self.account)

        self.assertIsInstance(planted_trees, list)
        self.assertEqual(len(planted_trees), 2)

        for planted_tree in planted_trees:
            self.assertIsInstance(planted_tree, PlantedTree)
            self.assertEqual(planted_tree.user, self.user)
            self.assertEqual(planted_tree.tree, self.tree)
            self.assertEqual(planted_tree.account, self.account)
            self.assertTrue(PlantedTree.objects.filter(
                pk=planted_tree.pk).exists())
